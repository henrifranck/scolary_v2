from typing import Any
import ast

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get('/', response_model=schemas.ResponseCmsPage)
def read_cms_pages(
    *,
    offset: int = 0,
    limit: int = 20,
    relation: str = "[]",
    where: str = "[]",
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve CMS pages.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    cms_pages = crud.cms_page.get_multi_where_array(
        db=db, relations=relations, skip=offset, limit=limit, where=wheres
    )
    count = crud.cms_page.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseCmsPage(
        **{"count": count, "data": jsonable_encoder(cms_pages)}
    )
    return response


@router.get('/public', response_model=schemas.ResponseCmsPage)
def read_public_cms_pages(
    *,
    offset: int = 0,
    limit: int = 200,
    relation: str = "[]",
    where: str = "[]",
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve CMS pages for public navigation.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
        relations += ast.literal_eval(relation)

    wheres = [
        {"key": "status", "operator": "=", "value": "published"}
    ]
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    cms_pages = crud.cms_page.get_multi_where_array(
        db=db, relations=relations, skip=offset, limit=limit, where=wheres
    )
    count = crud.cms_page.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseCmsPage(
        **{"count": count, "data": jsonable_encoder(cms_pages)}
    )
    return response


@router.post('/', response_model=schemas.CmsPage)
def create_cms_page(
    *,
    db: Session = Depends(deps.get_db),
    cms_page_in: schemas.CmsPageCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new CMS page.
    """
    cms_page = crud.cms_page.create(db=db, obj_in=cms_page_in)
    return cms_page


@router.put('/{cms_page_id}', response_model=schemas.CmsPage)
def update_cms_page(
    *,
    db: Session = Depends(deps.get_db),
    cms_page_id: int,
    cms_page_in: schemas.CmsPageUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a CMS page.
    """
    cms_page = crud.cms_page.get(db=db, id=cms_page_id)
    if not cms_page:
        raise HTTPException(status_code=404, detail='CmsPage not found')
    cms_page = crud.cms_page.update(db=db, db_obj=cms_page, obj_in=cms_page_in)
    return cms_page


@router.get('/{cms_page_id}', response_model=schemas.CmsPage)
def read_cms_page(
    *,
    relation: str = "[]",
    where: str = "[]",
    db: Session = Depends(deps.get_db),
    cms_page_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get CMS page by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    cms_page = crud.cms_page.get(db=db, id=cms_page_id, relations=relations, where=wheres)
    if not cms_page:
        raise HTTPException(status_code=404, detail='CmsPage not found')
    return cms_page


@router.delete('/{cms_page_id}', response_model=schemas.Msg)
def delete_cms_page(
    *,
    db: Session = Depends(deps.get_db),
    cms_page_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a CMS page.
    """
    cms_page = crud.cms_page.get(db=db, id=cms_page_id)
    if not cms_page:
        raise HTTPException(status_code=404, detail='CmsPage not found')
    crud.cms_page.remove(db=db, id=cms_page_id)
    return schemas.Msg(msg='CmsPage deleted successfully')


@router.get('/by_slug/{slug}', response_model=schemas.CmsPage)
def read_cms_page_by_slug(
    *,
    slug: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get CMS page by slug.
    """
    cms_page = crud.cms_page.get_by_slug(db=db, slug=slug)
    if not cms_page:
        raise HTTPException(status_code=404, detail='CmsPage not found')
    return cms_page
