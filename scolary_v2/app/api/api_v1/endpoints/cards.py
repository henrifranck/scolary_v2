import ast
import shutil
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api import deps
from app import crud, models, schemas

router = APIRouter()


@router.get('/', response_model=schemas.ResponseCard)
def read_cards(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    relations = []
    if relation:
        try:
            relations += ast.literal_eval(relation)
        except (ValueError, SyntaxError):
            pass

    wheres = []
    if where:
        try:
            wheres += ast.literal_eval(where)
        except (ValueError, SyntaxError):
            pass

    cards = crud.card.get_multi_where_array(
        db=db, relations=relations, skip=offset, limit=limit, where=wheres
    )
    count = crud.card.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseCard(**{'count': count, 'data': jsonable_encoder(cards)})
    return response


@router.post('/', response_model=schemas.Card)
def create_card(
        *,
        db: Session = Depends(deps.get_db),
        card_in: schemas.CardCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    return crud.card.create(db=db, obj_in=card_in)


@router.put('/{card_id}', response_model=schemas.Card)
def update_card(
        *,
        db: Session = Depends(deps.get_db),
        card_id: int,
        card_in: schemas.CardUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    card = crud.card.get(db=db, id=card_id)
    if not card:
        raise HTTPException(status_code=404, detail='Card not found')
    return crud.card.update(db=db, db_obj=card, obj_in=card_in)


@router.get('/{card_id}', response_model=schemas.Card)
def read_card(
        *,
        db: Session = Depends(deps.get_db),
        card_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    card = crud.card.get(db=db, id=card_id)
    if not card:
        raise HTTPException(status_code=404, detail='Card not found')
    return card


@router.delete('/{card_id}', response_model=schemas.Msg)
def delete_card(
        *,
        db: Session = Depends(deps.get_db),
        card_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    card = crud.card.get(db=db, id=card_id)
    if not card:
        raise HTTPException(status_code=404, detail='Card not found')
    crud.card.remove(db=db, id=card_id)
    return schemas.Msg(msg='Card deleted successfully')


@router.post('/upload-image', response_model=schemas.CardAsset)
def upload_card_image(
        *,
        db: Session = Depends(deps.get_db),
        file: UploadFile = File(...),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    if not file.filename:
        raise HTTPException(status_code=400, detail='No file provided')

    allowed_ext = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed_ext:
        raise HTTPException(status_code=400, detail='Unsupported file type')

    project_root = Path(__file__).resolve().parents[3]
    assets_dir = project_root / "assets" / "images"
    assets_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}{ext}"
    destination = assets_dir / filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    saved = crud.card_asset.create_with_user(
        db,
        obj_in=schemas.CardAssetCreate(
            filename=filename,
            path=f"assets/images/{filename}"
        ),
        uploaded_by_id=current_user.id if current_user else None
    )

    return saved

