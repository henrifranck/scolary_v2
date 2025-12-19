import shutil
from pathlib import Path
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, Query, Response
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.enum.file_type import FileTypeEnum

router = APIRouter()

FILES_ROOT = Path("files")
UPLOAD_DIR = FILES_ROOT / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _build_public_url(relative_path: str) -> str:
  normalized = str(relative_path or "").lstrip("/")
  if normalized.startswith("files/"):
    return f"/{normalized}"
  return f"/files/{normalized}"


def _serialize_file_asset(file_asset: models.FileAsset) -> schemas.FileAsset:
  return schemas.FileAsset(
    id=file_asset.id,
    name=file_asset.name,
    type=file_asset.type,
    size_bytes=file_asset.size_bytes,
    mime_type=file_asset.mime_type,
    path=file_asset.path,
    url=_build_public_url(file_asset.path),
    created_at=file_asset.created_at,
    updated_at=file_asset.updated_at,
  )


@router.get("/", response_model=schemas.ResponseFileAsset)
def list_files(
  *,
  offset: int = 0,
  limit: int = 20,
  q: Optional[str] = Query(None, description="Filter by partial name match"),
  file_type: Optional[FileTypeEnum] = Query(None, description="Filter by file type"),
  db: Session = Depends(deps.get_db),
  current_user: models.User = Depends(deps.get_current_active_user),
) -> schemas.ResponseFileAsset:
  wheres = []
  if q:
    wheres.append({"key": "name", "operator": "like", "value": q})
  if file_type:
    wheres.append({"key": "type", "operator": "==", "value": file_type})

  files: List[models.FileAsset] = crud.file_asset.get_multi_where_array(
    db=db,
    skip=offset,
    limit=limit,
    where=wheres,
  )
  count = crud.file_asset.get_count_where_array(db=db, where=wheres)

  return schemas.ResponseFileAsset(
    count=count,
    data=[_serialize_file_asset(file_asset) for file_asset in files],
  )


@router.get("/{file_id}/", response_model=schemas.FileAsset)
def read_file(
  *,
  file_id: int,
  db: Session = Depends(deps.get_db),
  current_user: models.User = Depends(deps.get_current_active_user),
) -> schemas.FileAsset:
  file_asset = crud.file_asset.get(db=db, id=file_id)
  if not file_asset:
    raise HTTPException(status_code=404, detail="File not found")
  return _serialize_file_asset(file_asset)


@router.post("/upload/", response_model=schemas.FileAsset)
def upload_file(
  *,
  db: Session = Depends(deps.get_db),
  file: UploadFile = File(...),
  name: Optional[str] = Form(None),
  type: Optional[FileTypeEnum] = Form(None),
  current_user: models.User = Depends(deps.get_current_active_user),
) -> schemas.FileAsset:
  if not file.filename:
    raise HTTPException(status_code=400, detail="No file provided")

  original_name = name or Path(file.filename).name
  extension = Path(file.filename).suffix
  safe_extension = extension if extension else ""
  filename = f"{uuid4().hex}{safe_extension}"

  UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
  destination = UPLOAD_DIR / filename
  with destination.open("wb") as buffer:
    shutil.copyfileobj(file.file, buffer)

  relative_path = destination.relative_to(FILES_ROOT)
  size_bytes = destination.stat().st_size

  created = crud.file_asset.create_with_uploader(
    db=db,
    obj_in=schemas.FileAssetCreate(
      name=original_name,
      path=str(relative_path).replace("\\", "/"),
      type=type or FileTypeEnum.OTHER,
      size_bytes=size_bytes,
      mime_type=file.content_type,
    ),
    uploaded_by_id=current_user.id if current_user else None,
  )

  return _serialize_file_asset(created)


@router.patch("/{file_id}/", response_model=schemas.FileAsset)
def update_file(
  *,
  file_id: int,
  file_in: schemas.FileAssetUpdate,
  db: Session = Depends(deps.get_db),
  current_user: models.User = Depends(deps.get_current_active_user),
) -> schemas.FileAsset:
  file_asset = crud.file_asset.get(db=db, id=file_id)
  if not file_asset:
    raise HTTPException(status_code=404, detail="File not found")

  updated = crud.file_asset.update(db=db, db_obj=file_asset, obj_in=file_in)
  return _serialize_file_asset(updated)


@router.delete("/{file_id}/", status_code=204)
def delete_file(
  *,
  file_id: int,
  db: Session = Depends(deps.get_db),
  current_user: models.User = Depends(deps.get_current_active_user),
) -> Response:
  file_asset = crud.file_asset.get(db=db, id=file_id)
  if not file_asset:
    raise HTTPException(status_code=404, detail="File not found")

  file_path = (FILES_ROOT / file_asset.path).resolve()
  try:
    files_root_resolved = FILES_ROOT.resolve()
    if files_root_resolved in file_path.parents or file_path == files_root_resolved:
      if file_path.exists():
        file_path.unlink()
  except Exception:
    # If path resolution fails, fall back to database delete only
    pass

  crud.file_asset.remove(db=db, id=file_id)
  return Response(status_code=204)
