import ast
import io
import math
import shutil
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from jinja2 import Template
from sqlalchemy.orm import Session
from weasyprint import HTML

from app.api import deps
from app import crud, models, schemas

router = APIRouter()


def _build_card_html(card: models.Card, data: Any, count: int) -> tuple[str, Path]:
    data = data or {}
    template = Template(card.html_template)
    rendered_html = template.render(**data)
    copies = max(1, count)
    pages_html_parts = []
    for start in range(0, copies, 8):
        chunk_size = min(8, copies - start)
        rows = max(1, math.ceil(chunk_size / 2))
        page_templates = ''.join(
            f"<div class='card-slot'>{rendered_html}</div>" for _ in range(chunk_size)
        )
        pages_html_parts.append(
            f"<div class='print-page' style='--rows:{rows};'>{page_templates}</div>"
        )
    pages_html = ''.join(pages_html_parts)
    project_root = Path(__file__).resolve().parents[3]
    assets_card = project_root / "assets" / "card"
    base_path = assets_card if assets_card.exists() else project_root
    base_href = f"<base href='file://{base_path}/'>"
    full_html = f"""
    <html>
        <head>
            <meta charset="utf-8" />
            {base_href}
            <style>
                @page {{
                    size: A4;
                    margin: 0;
                }}
                html, body {{
                    width: 210mm;
                    height: 297mm;
                    margin: 0;
                    padding: 0;
                }}
                body {{
                    padding: 4px;
                    box-sizing: border-box;
                    width: calc(210mm - 8px);
                    height: calc(297mm - 8px);
                }}
                .print-page {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    grid-template-rows: repeat(var(--rows), minmax(0, 1fr));
                    gap: 4px;
                    height: 100%;
                    width: 100%;
                    box-sizing: border-box;
                    align-items: stretch;
                    justify-items: stretch;
                }}
                .print-page:not(:last-child) {{
                    page-break-after: always;
                }}
                .card-slot {{
                    padding: 4px;
                    box-sizing: border-box;
                    page-break-inside: avoid;
                    border: 1px solid #000;
                    height: 100%;
                    width: 100%;
                }}
                {card.css_styles or ''}
            </style>
        </head>
        <body>
            {pages_html}
        </body>
    </html>
    """
    return full_html, base_path


def _render_custom_pdf(
        *,
        html_template: str,
        css_styles: str | None,
        data: Any,
        copies: int,
        page_size: str = "A4",
) -> tuple[bytes, str]:
    try:
        rendered_html = Template(html_template).render(**(data or {}))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Template rendering failed: {exc}")

    copies = max(1, copies)
    pages_html_parts = []
    for start in range(0, copies, 8):
        chunk_size = min(8, copies - start)
        rows = max(1, math.ceil(chunk_size / 2))
        page_templates = ''.join(
            f"<div class='card-slot'>{rendered_html}</div>" for _ in range(chunk_size)
        )
        pages_html_parts.append(
            f"<div class='print-page' style='--rows:{rows};'>{page_templates}</div>"
        )
    pages_html = ''.join(pages_html_parts)
    project_root = Path(__file__).resolve().parents[3]
    assets_card = project_root / "assets" / "card"
    base_path = assets_card if assets_card.exists() else project_root
    base_href = f"<base href='file://{base_path}/'>"
    full_html = f"""
    <html>
        <head>
            <meta charset="utf-8" />
            {base_href}
            <style>
                @page {{
                    size: {page_size};
                    margin: 0;
                }}
                html, body {{
                    width: 210mm;
                    height: 297mm;
                    margin: 0;
                    padding: 0;
                }}
                body {{
                    padding: 4px;
                    box-sizing: border-box;
                    width: calc(210mm - 8px);
                    height: calc(297mm - 8px);
                }}
                .print-page {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    grid-template-rows: repeat(var(--rows), minmax(0, 1fr));
                    gap: 4px;
                    height: 100%;
                    width: 100%;
                    box-sizing: border-box;
                    align-items: stretch;
                    justify-items: stretch;
                }}
                .print-page:not(:last-child) {{
                    page-break-after: always;
                }}
                .card-slot {{
                    padding: 4px;
                    box-sizing: border-box;
                    page-break-inside: avoid;
                    border: 1px solid #000;
                    height: 100%;
                    width: 100%;
                }}
                {css_styles or ''}
            </style>
        </head>
        <body>
            {pages_html}
        </body>
    </html>
    """

    pdf_bytes = HTML(string=full_html, base_url=str(base_path)).write_pdf()
    return pdf_bytes, str(base_path)


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


@router.post('/{card_id}/render')
def render_card_pdf(
        *,
        db: Session = Depends(deps.get_db),
        card_id: int,
        count: int = 4,
        payload: schemas.CardRenderRequest,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    card = crud.card.get(db=db, id=card_id)
    if not card:
        raise HTTPException(status_code=404, detail='Card not found')

    full_html, base_url = _build_card_html(card, payload.data, count)

    pdf_bytes = HTML(string=full_html, base_url=str(base_url)).write_pdf()
    filename = f"card_{card_id}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.post('/{card_id}/render/chromium')
def render_card_pdf_chromium(
        *,
        db: Session = Depends(deps.get_db),
        card_id: int,
        count: int = 4,
        payload: schemas.CardRenderRequest,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise HTTPException(
            status_code=501,
            detail="Playwright is not installed. Please install playwright to use Chromium rendering.",
        )

    card = crud.card.get(db=db, id=card_id)
    if not card:
        raise HTTPException(status_code=404, detail='Card not found')

    full_html, base_url = _build_card_html(card, payload.data, count)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(full_html, wait_until="load")
        pdf_bytes = page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,
        )
        browser.close()

    filename = f"card_{card_id}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.post('/render-pdf/')
def render_card_pdf_from_payload(
        *,
        payload: schemas.CardPdfRenderRequest,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    pdf_bytes, _ = _render_custom_pdf(
        html_template=payload.html_template,
        css_styles=payload.css_styles,
        data=payload.data,
        copies=payload.copies or 1,
        page_size=payload.page_size or "A4",
    )

    filename = "card_template.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
