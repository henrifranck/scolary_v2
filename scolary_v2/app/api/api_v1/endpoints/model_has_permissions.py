from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps


@router.get('/', response_model=schemas.ResponseModelHasPermission)
def read_model_has_permissions(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve model_has_permissions.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    model_has_permissions = crud.model_has_permission.get_multi_where_array(
        db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.model_has_permission.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseModelHasPermission(**{'count': count, 'data': jsonable_encoder(model_has_permissions)})
    return response


@router.post('/', response_model=schemas.ModelHasPermission)
def create_model_has_permission(
        *,
        db: Session = Depends(deps.get_db),
        model_has_permission_in: schemas.ModelHasPermissionCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new model_has_permission.
    """
    model_has_permission = crud.model_has_permission.create(db=db, obj_in=model_has_permission_in)
    return model_has_permission


@router.put('/{model_has_permission_id}', response_model=schemas.ModelHasPermission)
def update_model_has_permission(
        *,
        db: Session = Depends(deps.get_db),
        model_has_permission_id: int,
        model_has_permission_in: schemas.ModelHasPermissionUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an model_has_permission.
    """
    model_has_permission = crud.model_has_permission.get(db=db, id=model_has_permission_id)
    if not model_has_permission:
        raise HTTPException(status_code=404, detail='ModelHasPermission not found')
    model_has_permission = crud.model_has_permission.update(db=db, db_obj=model_has_permission,
                                                            obj_in=model_has_permission_in)
    return model_has_permission


@router.get('/{model_has_permission_id}', response_model=schemas.ModelHasPermission)
def read_model_has_permission(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        model_has_permission_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get model_has_permission by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    model_has_permission = crud.model_has_permission.get(db=db, id=model_has_permission_id, relations=relations,
                                                         where=wheres)
    if not model_has_permission:
        raise HTTPException(status_code=404, detail='ModelHasPermission not found')
    return model_has_permission


@router.delete('/{model_has_permission_id}', response_model=schemas.Msg)
def delete_model_has_permission(
        *,
        db: Session = Depends(deps.get_db),
        model_has_permission_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an model_has_permission.
    """
    model_has_permission = crud.model_has_permission.get(db=db, id=model_has_permission_id)
    if not model_has_permission:
        raise HTTPException(status_code=404, detail='ModelHasPermission not found')
    model_has_permission = crud.model_has_permission.remove(db=db, id=model_has_permission_id)
    return schemas.Msg(msg='ModelHasPermission deleted successfully')
