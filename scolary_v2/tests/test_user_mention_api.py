# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_user_mention_api(client, db):
    """Create UserMention via API."""
    # Auth setup
    user_data = {
        'email': 'NLXcz@c94yu.com',
        'last_name': 'Zc3jL',
        'password': 'zubfA',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for User
    user_data = schemas.UserCreate(
        email='8O5oK@goq5m.com',
        first_name='aEFod',
        last_name='JoY3O',
        password='0C1wr',
        is_superuser=True,
        picture='o2zi6',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='ubhQc',
        slug='Ck1q5',
        abbreviation='fZOy6',
        plugged='xaT1T',
        background='fenlP',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    user_mention_data = {
        'id_user': user.id,
        'id_mention': mention.id,
    }

    resp = client.post('/api/v1/user_mentions/', json=user_mention_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_user'] == user_mention_data['id_user']
    assert created['id_mention'] == user_mention_data['id_mention']


def test_update_user_mention_api(client, db):
    """Update UserMention via API."""
    # Auth setup
    user_data = {
        'email': 'tK7yg@zedqt.com',
        'last_name': 'VsNGq',
        'password': 'cUf8E',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for User
    user_data = schemas.UserCreate(
        email='7R4AG@0akef.com',
        first_name='o9wR8',
        last_name='RmVA6',
        password='t2l9d',
        is_superuser=False,
        picture='EMZq9',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='rilrR',
        slug='MvMcU',
        abbreviation='c4ALV',
        plugged='846nc',
        background='oJ32V',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    user_mention_data = {
        'id_user': user.id,
        'id_mention': mention.id,
    }

    # Precompute enum values for update
    enum_values_map = {}

    # Helper to compute a new value different from the current one (for API payload)
    def _updated_value(k, v):
        from decimal import Decimal

        # bool -> invert
        if isinstance(v, bool):
            return not v

        # numeric -> +1 (int, float, Decimal)
        if isinstance(v, (int, float, Decimal)):
            return v + 1

        # enum -> next value from enum_values_map
        if k in enum_values_map:
            current = v
            values = enum_values_map[k]
            try:
                idx = values.index(current)
                if len(values) > 1:
                    return values[(idx + 1) % len(values)]
                else:
                    return current
            except ValueError:
                # si la valeur actuelle n'est pas dans la liste, prendre la première
                return values[0] if values else v

        # datetime +1 jour
        if k in []:
            if isinstance(v, str):
                return (datetime.fromisoformat(v) + timedelta(days=1)).isoformat()
            return v

        # date +1 jour
        if k in []:
            if isinstance(v, str):
                return (date.fromisoformat(v) + timedelta(days=1)).isoformat()
            return v

        # time +1 heure
        if k in []:
            if isinstance(v, str):
                return (datetime.strptime(v, '%H:%M:%S') + timedelta(hours=1)).time().strftime('%H:%M:%S')
            return v

        # fallback -> prefix 'updated_'
        return f'updated_{v}'

    resp_c = client.post('/api/v1/user_mentions/', json=user_mention_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_user', 'id_mention']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in user_mention_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/user_mentions/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']


def test_get_user_mention_api(client, db):
    """Get UserMention via API."""
    # Auth setup
    user_data = {
        'email': 'yQBn2@rksaj.com',
        'last_name': '065X9',
        'password': '9nI47',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for User
    user_data = schemas.UserCreate(
        email='XHa9r@8pz0v.com',
        first_name='LIHug',
        last_name='3Dy68',
        password='kpaXe',
        is_superuser=False,
        picture='bQvZy',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='fEDTn',
        slug='aHncU',
        abbreviation='Yhi3S',
        plugged='O1dwj',
        background='PLyaP',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    user_mention_data = {
        'id_user': user.id,
        'id_mention': mention.id,
    }

    client.post('/api/v1/user_mentions/', json=user_mention_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/user_mentions/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_user_mention_api(client, db):
    """Get_by_id UserMention via API."""
    # Auth setup
    user_data = {
        'email': 'ORKZL@kqydk.com',
        'last_name': 'GaYu7',
        'password': 'u6Vyb',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for User
    user_data = schemas.UserCreate(
        email='qMlha@hfnew.com',
        first_name='JBmOi',
        last_name='LXepN',
        password='LSK4C',
        is_superuser=True,
        picture='zHLQo',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='BsLXj',
        slug='4e65l',
        abbreviation='1T91I',
        plugged='0c0hd',
        background='KjmSb',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    user_mention_data = {
        'id_user': user.id,
        'id_mention': mention.id,
    }

    resp_c = client.post('/api/v1/user_mentions/', json=user_mention_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/user_mentions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_user_mention_api(client, db):
    """Delete UserMention via API."""
    # Auth setup
    user_data = {
        'email': 'SOsrf@bsxe8.com',
        'last_name': 'NM38U',
        'password': '55WFS',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for User
    user_data = schemas.UserCreate(
        email='hlcTR@c7vzs.com',
        first_name='Q9QXD',
        last_name='SXwfr',
        password='MLTm7',
        is_superuser=True,
        picture='6yrkM',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='ZcJpw',
        slug='AYplU',
        abbreviation='4Q0wG',
        plugged='vAbEb',
        background='DWttj',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    user_mention_data = {
        'id_user': user.id,
        'id_mention': mention.id,
    }

    resp_c = client.post('/api/v1/user_mentions/', json=user_mention_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/user_mentions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'UserMention deleted successfully'
    resp_chk = client.get(f'/api/v1/user_mentions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #
