# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.schemas.role import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Role]:
        return db.query(Role).filter(getattr(Role, field) == value).first()

    def _normalize_relation_ids(self, ids: Optional[List[int]]) -> List[int]:
        if not ids:
            return []
        normalized = []
        for value in ids:
            if value is None:
                continue
            try:
                normalized.append(int(value))
            except (TypeError, ValueError):
                continue
        # Preserve order while removing duplicates
        return list(dict.fromkeys(normalized))

    def _sync_role_permissions(
            self,
            db: Session,
            *,
            role_id: int,
            permission_ids: Optional[List[int]],
            commit: bool = True,
    ) -> None:
        target_ids = set(self._normalize_relation_ids(permission_ids))
        if not target_ids and permission_ids is None:
            return

        existing_roles = db.query(RolePermission).filter(RolePermission.id_role == role_id).all()
        existing_ids = {ur.id_role for ur in existing_roles}

        for user_role in existing_roles:
            if user_role.id_role not in target_ids:
                db.delete(user_role)

        for permission_id in target_ids - existing_ids:
            db.add(RolePermission(id_role=role_id, id_permission=permission_id))

        if commit:
            db.commit()

    def create(self, db: Session, *, obj_in: RoleCreate) -> Role:
        obj_data = jsonable_encoder(obj_in)
        permission_ids = obj_data.pop('permission_ids', None)
        db_obj = Role(**obj_data)
        db.add(db_obj)
        db.flush()
        self._sync_role_permissions(db, role_id=db_obj.id, permission_ids=permission_ids, commit=False)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Role,
        obj_in: Union[RoleUpdate, Dict[str, Any]],
        commit: bool = True,
    ) -> Role:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in.copy()
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        permission_ids = update_data.pop('permission_ids', None)
        update_data["updated_at"] = func.now()

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.flush()
        self._sync_role_permissions(db, role_id=db_obj.id, permission_ids=permission_ids, commit=False)
        if commit:
            db.commit()
            db.refresh(db_obj)
        return db_obj


role = CRUDRole(Role)

# begin #
# ---write your code here--- #
# end #
