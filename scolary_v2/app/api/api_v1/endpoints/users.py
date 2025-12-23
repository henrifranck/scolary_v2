from typing import Any
from pathlib import Path
import uuid
import shutil

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
UPLOAD_DIR = Path("files") / "user_pictures"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg"}
@router.get('/', response_model=schemas.ResponseUser)
def read_users(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    users = crud.user.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.user.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseUser(**{'count': count, 'data': jsonable_encoder(users)})
    return response


@router.post('/', response_model=schemas.User)
def create_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.UserCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.create(db=db, obj_in=user_in)
    return user


@router.put('/{user_id}', response_model=schemas.User)
def update_user(
        *,
        db: Session = Depends(deps.get_db),
        user_id: int,
        user_in: schemas.UserUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an user.
    """
    user = crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    user = crud.user.update(db=db, db_obj=user, obj_in=user_in)
    return user


@router.get('/me', response_model=schemas.User)
def read_current_user(
        *,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get('/{user_id}', response_model=schemas.User)
def read_user(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        user_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get user by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    user = crud.user.get(db=db, id=user_id, relations=relations, where=wheres)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.delete('/{user_id}', response_model=schemas.Msg)
def delete_user(
        *,
        db: Session = Depends(deps.get_db),
        user_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an user.
    """
    user = crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    user = crud.user.remove(db=db, id=user_id)
    return schemas.Msg(msg='User deleted successfully')


@router.post('/{user_id}/picture', response_model=schemas.User)
async def upload_user_picture(
        *,
        db: Session = Depends(deps.get_db),
        user_id: int,
        file: UploadFile = File(...),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Upload and attach a profile picture to a user.
    """
    user = crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail='Unsupported file type')

    extension = Path(file.filename).suffix.lower()
    if extension not in {'.png', '.jpg', '.jpeg'}:
        extension = '.png' if file.content_type == 'image/png' else '.jpg'

    filename = f"{uuid.uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    relative_url = f"/files/user_pictures/{filename}"
    updated_user = crud.user.update(
        db=db,
        db_obj=user,
        obj_in={'picture': relative_url},
    )
    return updated_user
