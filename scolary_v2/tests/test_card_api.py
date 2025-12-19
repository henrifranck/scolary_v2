from fastapi import status
from app import crud, schemas
from app.core import security
import random


def _auth_headers(db):
    admin_data = {
        'email': f'card_admin_{random.randint(1, 10000)}@scolary.com',
        'last_name': 'Admin',
        'password': 'Secret1',
        'is_superuser': True,
        'is_active': True,
    }
    admin = crud.user.create(db, obj_in=schemas.UserCreate(**admin_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(admin.id), 'email': admin.email})
    return {"Authorization": f"Bearer {token}"}


def test_create_card_api(client, db):
    """Create a card template."""
    headers = _auth_headers(db)
    payload = {
        'name': 'Student Card Template',
        'card_type': 'student_card',
        'html_template': '<div>{{ full_name }}</div>',
        'css_styles': 'div { font-weight: bold; }',
    }
    resp = client.post('/api/v1/cards/', json=payload, headers=headers)
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['name'] == payload['name']
    assert created['card_type'] == payload['card_type']


def test_render_card_pdf_api(client, db):
    """Render a card template into PDF."""
    headers = _auth_headers(db)
    payload = {
        'name': 'Badge Template',
        'card_type': 'user_badge',
        'html_template': '<h1>{{ name }}</h1>',
        'css_styles': 'h1 { color: red; }',
    }
    resp_create = client.post('/api/v1/cards/', json=payload, headers=headers)
    card_id = resp_create.json()['id']

    resp_render = client.post(
        f'/api/v1/cards/{card_id}/render',
        json={'data': {'name': 'John Doe'}},
        headers=headers,
    )
    assert resp_render.status_code == status.HTTP_200_OK, resp_render.text
    assert resp_render.headers['content-type'] == 'application/pdf'
    assert resp_render.content.startswith(b'%PDF')
