#!/usr/bin/env python3
"""Migrate data from the legacy Scolary schema to the new schema.

This script expects both databases to already exist with their schemas.
Set OLD_DB_URL and NEW_DB_URL or pass --old-url/--new-url.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple

from sqlalchemy import MetaData, Table, create_engine, select, text
from sqlalchemy.engine import Connection

from dotenv import load_dotenv

from app.enum.register_type import RegisterTypeEnum

load_dotenv()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Migrate legacy Scolary data to new schema.")
    parser.add_argument("--old-url", default=os.getenv("OLD_DB_URL"))
    parser.add_argument("--new-url", default=os.getenv("NEW_DB_URL"))
    parser.add_argument("--batch-size", type=int, default=500)
    parser.add_argument("--truncate", action="store_true", help="Truncate target tables before insert.")
    parser.add_argument(
        "--ignore-existing",
        action="store_true",
        help="Use INSERT IGNORE to skip duplicates.",
    )
    return parser.parse_args()


def now_utc() -> dt.datetime:
    return dt.datetime.utcnow()


def clean_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.lower() in {"none", "null", ""}:
            return None
        return stripped
    return str(value)


def to_datetime(value: Any, fallback: dt.datetime) -> dt.datetime:
    if value is None:
        return fallback
    if isinstance(value, dt.datetime):
        return value
    if isinstance(value, dt.date):
        return dt.datetime.combine(value, dt.time())
    if isinstance(value, str):
        candidate = value.replace("Z", "").strip()
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return dt.datetime.strptime(candidate[:19], fmt)
            except ValueError:
                continue
        try:
            return dt.datetime.fromisoformat(candidate)
        except ValueError:
            return fallback
    return fallback


def to_date(value: Any, fallback: Optional[dt.date]) -> Optional[dt.date]:
    if value is None:
        return fallback
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        candidate = value.strip()
        if len(candidate) >= 10:
            try:
                return dt.date.fromisoformat(candidate[:10])
            except ValueError:
                pass
        if len(candidate) == 4 and candidate.isdigit():
            return dt.date(int(candidate), 1, 1)
    return fallback


def map_sex(value: Any) -> str:
    val = clean_str(value)
    if not val:
        return "MALE"
    lowered = val.lower()
    if lowered in {"f", "female", "feminin", "femme"}:
        return "FEMALE"
    return "MALE"


def map_martial_status(value: Any) -> str:
    val = clean_str(value)
    if not val:
        return "SINGLE"
    lowered = val.lower()
    if "mar" in lowered:
        return "MARRIED"
    if "div" in lowered:
        return "DIVORCED"
    if "veu" in lowered or "widow" in lowered:
        return "WIDOWED"
    return "SINGLE"


def map_repeat_status(value: Any) -> Optional[str]:
    val = clean_str(value)
    if not val:
        return None
    lowered = val.lower()
    if "pass" in lowered:
        return "PASSING"
    if "redoubl" in lowered or "repeat" in lowered:
        return "REPEATING"
    if "tripl" in lowered:
        return "TRIPLING"
    return None


def map_enrollment_status(status: Any, is_selected: Any) -> str:
    val = clean_str(status)
    if val in {"L1", "L2", "L3", "M1", "M2"}:
        return val
    if is_selected:
        return "selected"
    return "pending"


def normalize_session(value: Any) -> str:
    val = clean_str(value)
    if val in {"SR", "SN"}:
        return val
    return "SN"


def normalize_working_time_type(value: Any) -> str:
    val = clean_str(value)
    if not val:
        return "COURSE"
    lowered = val.lower()
    if lowered == "tp":
        return "TP"
    if lowered == "td":
        return "TD"
    if lowered == "exam":
        return "EXAM"
    return "COURSE"


def normalize_level(value: Any) -> Optional[str]:
    val = clean_str(value)
    if not val:
        return None
    upper = val.upper()
    if upper in {"L1", "L2", "L3", "M1", "M2"}:
        return upper
    return None


def dedupe_keyunique(value: Optional[str], row_id: Any, seen: set) -> Optional[str]:
    if not value:
        return None
    if value not in seen:
        seen.add(value)
        return value
    candidate = f"{value}-{row_id}"
    if candidate in seen:
        suffix = 1
        while f"{candidate}-{suffix}" in seen:
            suffix += 1
        candidate = f"{candidate}-{suffix}"
    seen.add(candidate)
    return candidate


def dedupe_field(value: Optional[str], row_id: Any, seen: set) -> Optional[str]:
    if not value:
        return None
    if value not in seen:
        seen.add(value)
        return value
    candidate = f"{value}-{row_id}"
    if candidate in seen:
        suffix = 1
        while f"{candidate}-{suffix}" in seen:
            suffix += 1
        candidate = f"{candidate}-{suffix}"
    seen.add(candidate)
    return candidate


def default_for_column(name: str, fallback_time: dt.datetime) -> Any:
    if name == "created_at":
        return fallback_time
    if name in {"updated_at", "deleted_at"}:
        return None
    if name in {"date_from", "date_to", "date_receipt"}:
        return fallback_time.date()
    if name == "semester":
        return "S1"
    if name == "session":
        return "SN"
    if name == "working_time_type":
        return "COURSE"
    if name == "sex":
        return "MALE"
    if name == "martial_status":
        return "SINGLE"
    if name == "enrollment_status":
        return "pending"
    if name == "repeat_status":
        return "PASSING"
    if name == "level":
        return "L1"
    if name in {"job", "address", "place_of_birth", "last_name"}:
        return "UNKNOWN" if name != "job" else ""
    if name in {"name", "slug", "abbreviation", "plugged"}:
        return "UNKNOWN"
    return "UNKNOWN"


def iter_rows(conn: Connection, table: Table, batch_size: int) -> Iterable[List[Any]]:
    result = conn.execution_options(stream_results=True).execute(select(table))
    while True:
        batch = result.fetchmany(batch_size)
        if not batch:
            return
        yield batch


def fill_missing_required(row: Dict[str, Any], target: Table, fallback_time: dt.datetime) -> Dict[str, Any]:
    for column in target.columns:
        if column.name in row:
            continue
        if not column.nullable and column.default is None and column.server_default is None:
            row[column.name] = default_for_column(column.name, fallback_time)
    return row


def migrate_table(
    conn_old: Connection,
    conn_new: Connection,
    meta_old: MetaData,
    meta_new: MetaData,
    target_name: str,
    source_name: Optional[str] = None,
    column_map: Optional[Dict[str, str]] = None,
    transform_row: Optional[Any] = None,
    batch_size: int = 500,
    ignore_existing: bool = False,
) -> None:
    source_name = source_name or target_name
    if source_name not in meta_old.tables:
        print(f"[skip] source table not found: {source_name}")
        return
    if target_name not in meta_new.tables:
        print(f"[skip] target table not found: {target_name}")
        return

    src = meta_old.tables[source_name]
    tgt = meta_new.tables[target_name]
    insert_stmt = tgt.insert()
    if ignore_existing:
        insert_stmt = insert_stmt.prefix_with("IGNORE")

    print(f"[migrate] {source_name} -> {target_name}")
    fallback_time = now_utc()

    for batch in iter_rows(conn_old, src, batch_size):
        rows: List[Dict[str, Any]] = []
        for item in batch:
            src_row = dict(item._mapping)
            data: Dict[str, Any] = {}
            for column in tgt.columns:
                src_key = column_map.get(column.name, column.name) if column_map else column.name
                if src_key in src_row:
                    data[column.name] = src_row[src_key]
            if transform_row:
                data = transform_row(data, src_row, fallback_time)
            data = fill_missing_required(data, tgt, fallback_time)
            rows.append(data)
        if rows:
            conn_new.execute(insert_stmt, rows)


def migrate_teaching_units(
    conn_old: Connection,
    conn_new: Connection,
    meta_old: MetaData,
    meta_new: MetaData,
    batch_size: int,
    ignore_existing: bool,
) -> None:
    if "teaching_unit" not in meta_old.tables or "teaching_unit" not in meta_new.tables:
        print("[skip] teaching_unit table missing")
        return
    if "teaching_unit_offering" not in meta_new.tables:
        print("[skip] teaching_unit_offering table missing")
        return

    src = meta_old.tables["teaching_unit"]
    tgt = meta_new.tables["teaching_unit"]
    offering = meta_new.tables["teaching_unit_offering"]
    insert_tgt = tgt.insert().prefix_with("IGNORE") if ignore_existing else tgt.insert()
    insert_off = offering.insert().prefix_with("IGNORE") if ignore_existing else offering.insert()
    fallback_time = now_utc()
    seen_keyunique: set = set()
    has_key_unique = "key_unique" in tgt.c

    print("[migrate] teaching_unit -> teaching_unit + teaching_unit_offering")
    for batch in iter_rows(conn_old, src, batch_size):
        base_rows: List[Dict[str, Any]] = []
        offer_rows: List[Dict[str, Any]] = []
        for item in batch:
            src_row = dict(item._mapping)
            created_at = to_datetime(src_row.get("created_at"), fallback_time)
            updated_at = to_datetime(src_row.get("updated_at"), fallback_time)
            unit_id = src_row.get("id")
            key_unique_val = None
            if has_key_unique:
                key_unique_val = dedupe_keyunique(
                    clean_str(src_row.get("key_unique")), unit_id, seen_keyunique
                )
            base_row = {
                "id": unit_id,
                "name": clean_str(src_row.get("title")) or "UNKNOWN",
                "semester": clean_str(src_row.get("semester")) or "S1",
                "id_journey": src_row.get("id_journey"),
                "created_at": created_at,
                "updated_at": updated_at,
                "deleted_at": None,
            }
            if has_key_unique:
                base_row["key_unique"] = key_unique_val
            base_rows.append(base_row)
            offer_rows.append(
                {
                    "id": unit_id,
                    "id_teaching_unit": unit_id,
                    "credit": src_row.get("credit") or 0,
                    "id_academic_year": None,
                    "id_teaching_unit_goup": None,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "deleted_at": None,
                }
            )
        if base_rows:
            conn_new.execute(insert_tgt, base_rows)
            conn_new.execute(insert_off, offer_rows)


def migrate_constituent_elements(
    conn_old: Connection,
    conn_new: Connection,
    meta_old: MetaData,
    meta_new: MetaData,
    batch_size: int,
    ignore_existing: bool,
) -> None:
    if "constituent_element" not in meta_old.tables or "constituent_element" not in meta_new.tables:
        print("[skip] constituent_element table missing")
        return
    if "constituent_element_offering" not in meta_new.tables:
        print("[skip] constituent_element_offering table missing")
        return

    src = meta_old.tables["constituent_element"]
    tgt = meta_new.tables["constituent_element"]
    offering = meta_new.tables["constituent_element_offering"]
    insert_tgt = tgt.insert().prefix_with("IGNORE") if ignore_existing else tgt.insert()
    insert_off = offering.insert().prefix_with("IGNORE") if ignore_existing else offering.insert()
    fallback_time = now_utc()
    seen_keyunique: set = set()
    has_key_unique = "key_unique" in tgt.c

    print("[migrate] constituent_element -> constituent_element + constituent_element_offering")
    for batch in iter_rows(conn_old, src, batch_size):
        base_rows: List[Dict[str, Any]] = []
        offer_rows: List[Dict[str, Any]] = []
        for item in batch:
            src_row = dict(item._mapping)
            created_at = to_datetime(src_row.get("created_at"), fallback_time)
            updated_at = to_datetime(src_row.get("updated_at"), fallback_time)
            elem_id = src_row.get("id")
            key_unique_val = None
            if has_key_unique:
                key_unique_val = dedupe_keyunique(
                    clean_str(src_row.get("key_unique")), elem_id, seen_keyunique
                )
            base_row = {
                "id": elem_id,
                "name": clean_str(src_row.get("title")) or "UNKNOWN",
                "semester": clean_str(src_row.get("semester")) or "S1",
                "id_journey": src_row.get("id_journey"),
                "color": clean_str(src_row.get("color")),
                "created_at": created_at,
                "updated_at": updated_at,
                "deleted_at": None,
            }
            if has_key_unique:
                base_row["key_unique"] = key_unique_val
            base_rows.append(base_row)
            offer_rows.append(
                {
                    "id": elem_id,
                    "id_constituent_element": elem_id,
                    "weight": src_row.get("weight") or 0,
                    "id_academic_year": None,
                    "id_constituent_element_optional_group": None,
                    "id_teching_unit_offering": src_row.get("id_teaching_unit"),
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "deleted_at": None,
                }
            )
        if base_rows:
            conn_new.execute(insert_tgt, base_rows)
            conn_new.execute(insert_off, offer_rows)


def migrate_students(
    conn_old: Connection,
    conn_new: Connection,
    meta_old: MetaData,
    meta_new: MetaData,
    batch_size: int,
    ignore_existing: bool,
) -> None:
    if "student" not in meta_old.tables or "student" not in meta_new.tables:
        print("[skip] student table missing")
        return
    src = meta_old.tables["student"]
    tgt = meta_new.tables["student"]
    insert_stmt = tgt.insert().prefix_with("IGNORE") if ignore_existing else tgt.insert()
    fallback_time = now_utc()
    seen_bacc: set = set()
    seen_cin: set = set()

    print("[migrate] student -> student")
    for batch in iter_rows(conn_old, src, batch_size):
        rows: List[Dict[str, Any]] = []
        for item in batch:
            src_row = dict(item._mapping)
            student_id = src_row.get("id")
            created_at = to_datetime(src_row.get("created_at"), fallback_time)
            updated_at = to_datetime(src_row.get("updated_at"), fallback_time)

            bacc_num_raw = clean_str(src_row.get("baccalaureate_num")) or f"UNK-{student_id}"
            bacc_num = dedupe_field(bacc_num_raw, student_id, seen_bacc)
            bacc_center = clean_str(src_row.get("baccalaureate_center")) or "UNKNOWN"
            num_select = clean_str(src_row.get("num_select")) or f"SEL-{student_id}"
            date_birth = to_date(src_row.get("date_birth"), fallback_time.date())
            date_cin = to_date(src_row.get("date_cin"), None)
            bacc_year = to_date(src_row.get("baccalaureate_years"), None)

            cin_raw = clean_str(src_row.get("num_cin"))
            cin_val = dedupe_field(cin_raw, student_id, seen_cin)

            rows.append(
                {
                    "id": student_id,
                    "num_carte": clean_str(src_row.get("num_carte")),
                    "email": clean_str(src_row.get("email")),
                    "num_select": num_select,
                    "last_name": clean_str(src_row.get("last_name")) or "UNKNOWN",
                    "first_name": clean_str(src_row.get("first_name")),
                    "date_of_birth": date_birth,
                    "place_of_birth": clean_str(src_row.get("place_birth")) or "UNKNOWN",
                    "address": clean_str(src_row.get("address")) or "UNKNOWN",
                    "sex": map_sex(src_row.get("sex")),
                    "martial_status": map_martial_status(src_row.get("situation")),
                    "phone_number": clean_str(src_row.get("telephone")),
                    "num_of_cin": cin_val,
                    "date_of_cin": date_cin,
                    "place_of_cin": clean_str(src_row.get("place_cin")),
                    "repeat_status": map_repeat_status(src_row.get("type")),
                    "picture": clean_str(src_row.get("photo")),
                    "num_of_baccalaureate": bacc_num,
                    "center_of_baccalaureate": bacc_center,
                    "year_of_baccalaureate": bacc_year,
                    "job": clean_str(src_row.get("work")) or "",
                    "father_name": clean_str(src_row.get("father_name")),
                    "father_job": clean_str(src_row.get("father_work")),
                    "mother_name": clean_str(src_row.get("mother_name")),
                    "mother_job": clean_str(src_row.get("mother_work")),
                    "parent_address": clean_str(src_row.get("parent_address")),
                    "level": normalize_level(src_row.get("level")),
                    "mean": src_row.get("mean"),
                    "enrollment_status": map_enrollment_status(
                        src_row.get("status"), src_row.get("is_selected")
                    ),
                    "imported_id": clean_str(src_row.get("import_id")),
                    "id_mention": src_row.get("id_mention"),
                    "id_enter_year": src_row.get("enter_years"),
                    "id_nationality": src_row.get("nationality_id"),
                    "id_baccalaureate_series": src_row.get("baccalaureate_series_id"),
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "deleted_at": None,
                }
            )
        if rows:
            conn_new.execute(insert_stmt, rows)


def migrate_user_roles(
    conn_old: Connection,
    conn_new: Connection,
    meta_old: MetaData,
    meta_new: MetaData,
    batch_size: int,
    ignore_existing: bool,
) -> None:
    if "user" not in meta_old.tables or "user_role" not in meta_new.tables:
        print("[skip] user_role table missing")
        return

    src = meta_old.tables["user"]
    tgt = meta_new.tables["user_role"]
    insert_stmt = tgt.insert().prefix_with("IGNORE") if ignore_existing else tgt.insert()
    fallback_time = now_utc()

    print("[migrate] user.id_role -> user_role")
    for batch in iter_rows(conn_old, src, batch_size):
        rows: List[Dict[str, Any]] = []
        for item in batch:
            src_row = dict(item._mapping)
            role_id = src_row.get("id_role")
            if not role_id:
                continue
            created_at = to_datetime(src_row.get("created_at"), fallback_time)
            rows.append(
                {
                    "id_user": src_row.get("id"),
                    "id_role": role_id,
                    "created_at": created_at,
                    "updated_at": to_datetime(src_row.get("updated_at"), fallback_time),
                    "deleted_at": None,
                }
            )
        if rows:
            conn_new.execute(insert_stmt, rows)


def migrate_student_years(
    conn_old: Connection,
    conn_new: Connection,
    meta_old: MetaData,
    meta_new: MetaData,
    batch_size: int,
    ignore_existing: bool,
) -> Dict[Tuple[str, int], int]:
    if "student_years" not in meta_old.tables:
        print("[skip] student_years table missing")
        return {}
    if "annual_register" not in meta_new.tables or "register_semester" not in meta_new.tables:
        print("[skip] annual_register/register_semester tables missing")
        return {}

    src = meta_old.tables["student_years"]
    annual = meta_new.tables["annual_register"]
    register = meta_new.tables["register_semester"]
    insert_annual = annual.insert().prefix_with("IGNORE") if ignore_existing else annual.insert()
    insert_register = register.insert().prefix_with("IGNORE") if ignore_existing else register.insert()
    fallback_time = now_utc()

    lookup: Dict[Tuple[str, int], int] = {}
    seen_keys: Dict[Tuple[str, int], int] = {}
    skipped = 0

    print("[migrate] student_years -> annual_register + register_semester")
    for batch in iter_rows(conn_old, src, batch_size):
        annual_rows: List[Dict[str, Any]] = []
        register_rows: List[Dict[str, Any]] = []
        for item in batch:
            src_row = dict(item._mapping)
            annual_id = src_row.get("id")
            num_carte = clean_str(src_row.get("num_carte"))
            id_year = src_row.get("id_year")
            key = (num_carte, id_year)
            if num_carte and id_year is not None:
                if key in seen_keys:
                    lookup[key] = seen_keys[key]
                    skipped += 1
                    continue
                seen_keys[key] = annual_id
                lookup[key] = annual_id

            created_at = to_datetime(src_row.get("created_at"), fallback_time)
            updated_at = to_datetime(src_row.get("updated_at"), fallback_time)
            inf_sem = clean_str(src_row.get("inf_semester"))
            sup_sem = clean_str(src_row.get("sup_semester"))
            semester_count = 1
            if inf_sem and sup_sem and inf_sem != sup_sem:
                semester_count = 2

            annual_rows.append(
                {
                    "id": annual_id,
                    "num_carte": num_carte,
                    "id_academic_year": id_year,
                    "register_type":"REGISTRATION",
                    "semester_count": semester_count,
                    "id_enrollment_fee": None,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "deleted_at": None,
                }
            )

            register_rows.append(
                {
                    "id_annual_register": annual_id,
                    "semester": clean_str(src_row.get("active_semester"))
                    or inf_sem
                    or "S1",
                    "repeat_status": map_repeat_status(src_row.get("status")) or "PASSING",
                    "id_journey": src_row.get("id_journey"),
                    "imported_id": clean_str(src_row.get("import_id")),
                    "is_valid": None,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "deleted_at": None,
                }
            )

        if annual_rows:
            conn_new.execute(insert_annual, annual_rows)
            conn_new.execute(insert_register, register_rows)

    if skipped:
        print(f"[warn] skipped {skipped} duplicate annual_register entries")

    return lookup


def migrate_subscription_types(
    conn_old: Connection,
    conn_new: Connection,
    meta_old: MetaData,
    meta_new: MetaData,
    batch_size: int,
    ignore_existing: bool,
) -> None:
    if "subscription_type" not in meta_old.tables or "subscription" not in meta_new.tables:
        print("[skip] subscription_type/subscription tables missing")
        return

    src = meta_old.tables["subscription_type"]
    tgt = meta_new.tables["subscription"]
    insert_stmt = tgt.insert().prefix_with("IGNORE") if ignore_existing else tgt.insert()
    fallback_time = now_utc()

    print("[migrate] subscription_type -> subscription")
    for batch in iter_rows(conn_old, src, batch_size):
        rows: List[Dict[str, Any]] = []
        for item in batch:
            src_row = dict(item._mapping)
            rows.append(
                {
                    "id": src_row.get("id"),
                    "name": clean_str(src_row.get("name")) or "UNKNOWN",
                    "created_at": to_datetime(src_row.get("created_at"), fallback_time),
                    "updated_at": to_datetime(src_row.get("updated_at"), fallback_time),
                    "deleted_at": None,
                }
            )
        if rows:
            conn_new.execute(insert_stmt, rows)


def migrate_student_subscriptions(
    conn_old: Connection,
    conn_new: Connection,
    meta_old: MetaData,
    meta_new: MetaData,
    annual_lookup: Dict[Tuple[str, int], int],
    batch_size: int,
    ignore_existing: bool,
) -> None:
    if "subscription" not in meta_old.tables or "student_subscription" not in meta_new.tables:
        print("[skip] subscription/student_subscription tables missing")
        return

    src = meta_old.tables["subscription"]
    tgt = meta_new.tables["student_subscription"]
    insert_stmt = tgt.insert().prefix_with("IGNORE") if ignore_existing else tgt.insert()
    fallback_time = now_utc()

    print("[migrate] subscription -> student_subscription")
    skipped = 0
    for batch in iter_rows(conn_old, src, batch_size):
        rows: List[Dict[str, Any]] = []
        for item in batch:
            src_row = dict(item._mapping)
            key = (clean_str(src_row.get("num_carte")) or "", src_row.get("id_year"))
            annual_id = annual_lookup.get(key)
            if not annual_id:
                skipped += 1
                continue
            rows.append(
                {
                    "id_subscription": src_row.get("subscription_type_id"),
                    "id_annual_register": annual_id,
                    "created_at": to_datetime(src_row.get("created_at"), fallback_time),
                    "updated_at": to_datetime(src_row.get("updated_at"), fallback_time),
                    "deleted_at": None,
                }
            )
        if rows:
            conn_new.execute(insert_stmt, rows)
    if skipped:
        print(f"[warn] skipped {skipped} subscriptions without matching annual_register")


def migrate_payments(
    conn_old: Connection,
    conn_new: Connection,
    meta_old: MetaData,
    meta_new: MetaData,
    annual_lookup: Dict[Tuple[str, int], int],
    batch_size: int,
    ignore_existing: bool,
) -> None:
    if "student_receipt" not in meta_old.tables or "payment" not in meta_new.tables:
        print("[skip] student_receipt/payment tables missing")
        return

    src = meta_old.tables["student_receipt"]
    tgt = meta_new.tables["payment"]
    insert_stmt = tgt.insert().prefix_with("IGNORE") if ignore_existing else tgt.insert()
    fallback_time = now_utc()
    seen_receipt: set = set()

    print("[migrate] student_receipt -> payment")
    skipped = 0
    for batch in iter_rows(conn_old, src, batch_size):
        rows: List[Dict[str, Any]] = []
        for item in batch:
            src_row = dict(item._mapping)
            key = (clean_str(src_row.get("num_carte")) or "", src_row.get("id_year"))
            annual_id = annual_lookup.get(key)
            if not annual_id:
                skipped += 1
                continue
            date_receipt = to_date(src_row.get("date"), fallback_time.date())
            receipt_raw = clean_str(src_row.get("num")) or "UNKNOWN"
            receipt_num = dedupe_field(receipt_raw, src_row.get("id"), seen_receipt)
            rows.append(
                {
                    "id_annual_register": annual_id,
                    "payed": src_row.get("payed") or 0,
                    "num_receipt": receipt_num,
                    "date_receipt": date_receipt,
                    "description": "Droit d'inscription",
                    "created_at": to_datetime(src_row.get("created_at"), fallback_time),
                    "updated_at": to_datetime(src_row.get("updated_at"), fallback_time),
                    "deleted_at": None,
                }
            )
        if rows:
            conn_new.execute(insert_stmt, rows)
    if skipped:
        print(f"[warn] skipped {skipped} receipts without matching annual_register")


def transform_exam_date(data: Dict[str, Any], src: Dict[str, Any], fallback_time: dt.datetime) -> Dict[str, Any]:
    data["date_from"] = to_date(src.get("date_from"), fallback_time.date())
    data["date_to"] = to_date(src.get("date_to"), fallback_time.date())
    data["session"] = normalize_session(src.get("session"))
    data["created_at"] = to_datetime(src.get("created_at"), fallback_time)
    data["updated_at"] = to_datetime(src.get("updated_at"), fallback_time)
    return data


def transform_exam_group(data: Dict[str, Any], src: Dict[str, Any], fallback_time: dt.datetime) -> Dict[str, Any]:
    data["semester"] = clean_str(src.get("semester")) or "S1"
    data["num_from"] = src.get("num_from") or 0
    data["num_to"] = src.get("num_to") or 0
    data["session"] = normalize_session(src.get("session"))
    data["created_at"] = to_datetime(src.get("created_at"), fallback_time)
    data["updated_at"] = to_datetime(src.get("updated_at"), fallback_time)
    return data


def transform_working_time(data: Dict[str, Any], src: Dict[str, Any], fallback_time: dt.datetime) -> Dict[str, Any]:
    data["working_time_type"] = normalize_working_time_type(src.get("type"))
    data["session"] = normalize_session(src.get("session"))
    data["created_at"] = to_datetime(src.get("created_at"), fallback_time)
    data["updated_at"] = to_datetime(src.get("updated_at"), fallback_time)
    return data


def transform_enrollment_fee(data: Dict[str, Any], src: Dict[str, Any], fallback_time: dt.datetime) -> Dict[str, Any]:
    data["level"] = src.get("level")
    data["register_type"] = RegisterTypeEnum.REGISTRATION
    data["created_at"] = to_datetime(src.get("created_at"), fallback_time)
    data["updated_at"] = to_datetime(src.get("updated_at"), fallback_time)
    return data


def transform_role(data: Dict[str, Any], src: Dict[str, Any], fallback_time: dt.datetime) -> Dict[str, Any]:
    data["name"] = clean_str(src.get("title")) or "UNKNOWN"
    data["created_at"] = to_datetime(src.get("created_at"), fallback_time)
    data["updated_at"] = to_datetime(src.get("updated_at"), fallback_time)
    data["use_for_card"] = 0
    return data


def transform_user(data: Dict[str, Any], src: Dict[str, Any], fallback_time: dt.datetime) -> Dict[str, Any]:
    data["email"] = clean_str(src.get("email")) or f"no-email-{src.get('id')}@local"
    data["first_name"] = clean_str(src.get("first_name"))
    data["last_name"] = clean_str(src.get("last_name")) or "UNKNOWN"
    data["hashed_password"] = clean_str(src.get("hashed_password")) or ""
    data["picture"] = clean_str(src.get("photo")) or clean_str(src.get("photo_url"))
    data["created_at"] = to_datetime(src.get("created_at"), fallback_time)
    data["updated_at"] = to_datetime(src.get("updated_at"), fallback_time)
    return data


def transform_mention(data: Dict[str, Any], src: Dict[str, Any], fallback_time: dt.datetime) -> Dict[str, Any]:
    data["name"] = clean_str(src.get("title")) or "UNKNOWN"
    data["slug"] = clean_str(src.get("value")) or "unknown"
    data["created_at"] = to_datetime(src.get("created_at"), fallback_time)
    data["updated_at"] = to_datetime(src.get("updated_at"), fallback_time)
    return data


def transform_journey(data: Dict[str, Any], src: Dict[str, Any], fallback_time: dt.datetime) -> Dict[str, Any]:
    data["name"] = clean_str(src.get("title")) or "UNKNOWN"
    data["created_at"] = to_datetime(src.get("created_at"), fallback_time)
    data["updated_at"] = to_datetime(src.get("updated_at"), fallback_time)
    return data


def transform_simple_dates(data: Dict[str, Any], src: Dict[str, Any], fallback_time: dt.datetime) -> Dict[str, Any]:
    data["created_at"] = to_datetime(src.get("created_at"), fallback_time)
    data["updated_at"] = to_datetime(src.get("updated_at"), fallback_time)
    return data


def migrate_all(args: argparse.Namespace) -> None:
    if not args.old_url or not args.new_url:
        print("Missing DB URLs. Provide --old-url and --new-url or set OLD_DB_URL/NEW_DB_URL.")
        sys.exit(2)

    engine_old = create_engine(args.old_url)
    engine_new = create_engine(args.new_url)

    meta_old = MetaData()
    meta_new = MetaData()
    meta_old.reflect(bind=engine_old)
    meta_new.reflect(bind=engine_new)

    with engine_old.connect() as conn_old, engine_new.begin() as conn_new:
        conn_new.execute(text("SET FOREIGN_KEY_CHECKS=0"))

        if args.truncate:
            for table_name in meta_new.tables:
                conn_new.execute(text(f"TRUNCATE TABLE `{table_name}`"))

        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="academic_year",
            source_name="college_year",
            column_map={"name": "title", "code": "code", "created_at": "created_at", "updated_at": "updated_at"},
            transform_row=transform_simple_dates,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="baccalaureate_serie",
            source_name="baccserie",
            column_map={
                "name": "title",
                "value": "value",
                "created_at": "created_at",
                "updated_at": "updated_at",
            },
            transform_row=transform_simple_dates,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="classroom",
            source_name="classroom",
            column_map={
                "name": "name",
                "capacity": "capacity",
                "created_at": "created_at",
                "updated_at": "updated_at",
            },
            transform_row=transform_simple_dates,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="mention",
            source_name="mention",
            column_map={
                "name": "title",
                "slug": "value",
                "abbreviation": "abbreviation",
                "plugged": "plugged",
                "background": "background_image",
                "created_at": "created_at",
                "updated_at": "updated_at",
            },
            transform_row=transform_mention,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="journey",
            source_name="journey",
            column_map={
                "name": "title",
                "abbreviation": "abbreviation",
                "id_mention": "id_mention",
                "created_at": "created_at",
                "updated_at": "updated_at",
            },
            transform_row=transform_journey,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="journey_semester",
            source_name="journey_semester",
            column_map={
                "id_journey": "id_journey",
                "semester": "semester",
                "created_at": "created_at",
                "updated_at": "updated_at",
            },
            transform_row=transform_simple_dates,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="nationality",
            source_name="nationality",
            column_map={"name": "name", "created_at": "created_at", "updated_at": "updated_at"},
            transform_row=transform_simple_dates,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="university",
            source_name="university_info",
            column_map={
                "province": "province",
                "department_name": "department_name",
                "department_other_information": "department_other_information",
                "department_address": "department_address",
                "email": "email",
                "logo_university": "logo_univ",
                "logo_departement": "logo_depart",
                "phone_number": "phone_number",
                "admin_signature": "admin_signature",
                "created_at": "created_at",
                "updated_at": "updated_at",
            },
            transform_row=transform_simple_dates,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )

        migrate_teaching_units(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_constituent_elements(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )

        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="exam_date",
            source_name="exam_date",
            column_map={
                "id_academic_year": "id_year",
                "date_from": "date_from",
                "date_to": "date_to",
                "session": "session",
                "created_at": "created_at",
                "updated_at": "updated_at",
            },
            transform_row=transform_exam_date,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="exam_group",
            source_name="exam_group",
            column_map={
                "id_classroom": "id_classroom",
                "id_journey": "id_journey",
                "semester": "semester",
                "num_from": "num_from",
                "num_to": "num_to",
                "session": "session",
                "id_accademic_year": "id_year",
                "created_at": "created_at",
                "updated_at": "updated_at",
            },
            transform_row=transform_exam_group,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )

        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="enrollment_fee",
            source_name="enrollment_fee",
            column_map={
                "level": "level",
                "price": "price",
                "id_mention": "id_mention",
                "register_type": "register_type",
                "id_academic_year": "id_year",
                "created_at": "created_at",
                "updated_at": "updated_at",

            },
            transform_row=transform_enrollment_fee,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )

        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="group",
            source_name="student_group",
            column_map={
                "id_journey": "id_journey",
                "semester": "semester",
                "group_number": "group_count",
                "student_count": "student_count",
                "created_at": "created_at",
                "updated_at": "updated_at",
            },
            transform_row=transform_simple_dates,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )

        migrate_students(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )

        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="role",
            source_name="role",
            column_map={"name": "title", "created_at": "created_at", "updated_at": "updated_at"},
            transform_row=transform_role,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="user",
            source_name="user",
            column_map={
                "email": "email",
                "first_name": "first_name",
                "last_name": "last_name",
                "hashed_password": "hashed_password",
                "is_superuser": "is_superuser",
                "picture": "photo",
                "is_active": "is_active",
                "created_at": "created_at",
                "updated_at": "updated_at",
            },
            transform_row=transform_user,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="user_mention",
            source_name="user_mention",
            column_map={
                "id_user": "id_user",
                "id_mention": "id_mention",
                "created_at": "created_at",
                "updated_at": "updated_at",
            },
            transform_row=transform_simple_dates,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_user_roles(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )

        migrate_table(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            target_name="working_time",
            source_name="working_time",
            column_map={
                "id_constituent_element": "id_constituent_element",
                "working_time_type": "type",
                "day": "day",
                "start": "start",
                "end": "end",
                "id_group": "group",
                "date": "date",
                "session": "session",
                "created_at": "created_at",
                "updated_at": "updated_at",
            },
            transform_row=transform_working_time,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )

        annual_lookup = migrate_student_years(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_subscription_types(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_student_subscriptions(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            annual_lookup=annual_lookup,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )
        migrate_payments(
            conn_old,
            conn_new,
            meta_old,
            meta_new,
            annual_lookup=annual_lookup,
            batch_size=args.batch_size,
            ignore_existing=args.ignore_existing,
        )

        conn_new.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def main() -> None:
    args = parse_args()
    migrate_all(args)


if __name__ == "__main__":
    main()
