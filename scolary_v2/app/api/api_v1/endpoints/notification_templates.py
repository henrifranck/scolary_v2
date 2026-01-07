from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app import crud, models, schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.NotificationTemplateOut])
def list_notification_templates(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    templates = crud.notification_template.get_multi_where_array(db=db, skip=0, limit=1000)
    return templates


@router.post("/", response_model=schemas.NotificationTemplateOut)
def create_notification_template(
    payload: schemas.NotificationTemplateCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    existing = crud.notification_template.get_by_key(db=db, key=payload.key)
    if existing:
        raise HTTPException(
            status_code=400, detail="A template with this key already exists."
        )
    return crud.notification_template.create(db=db, obj_in=payload)


@router.put("/{template_id}", response_model=schemas.NotificationTemplateOut)
def update_notification_template(
    template_id: int,
    payload: schemas.NotificationTemplateUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    template = crud.notification_template.get(db=db, id=template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return crud.notification_template.update(db=db, db_obj=template, obj_in=payload)


@router.delete("/{template_id}")
def delete_notification_template(
    template_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    template = crud.notification_template.get(db=db, id=template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    crud.notification_template.remove(db=db, id=template_id)
    return {"status": "ok"}
