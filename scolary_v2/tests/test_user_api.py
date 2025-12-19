# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from app.models.user_role import UserRole
from app.models.user_mention import UserMention
from datetime import datetime, timedelta, date, time
from io import BytesIO
from pathlib import Path
import random
from app.core import security


def test_create_user_api(client, db):
    """Create User via API."""
    # Auth setup
    user_data = {
        'email': 'cxNoW@s8rv0.com',
        'last_name': 'TQKyE',
        'password': 'AnJOj',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    user_data = {
        'email': 'k9Xja@gjg1k.com',
        'first_name': 'tDtqR',
        'last_name': 'TGNVR',
        'password': 'FR35E',
        'is_superuser': True,
        'picture': 'Huvky',
        'is_active': False,
    }

    resp = client.post('/api/v1/users/', json=user_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['email'] == user_data['email']
    assert created['first_name'] == user_data['first_name']
    assert created['last_name'] == user_data['last_name']
    assert created['is_superuser'] == user_data['is_superuser']
    assert created['picture'] == user_data['picture']
    assert created['is_active'] == user_data['is_active']


def test_update_user_api(client, db):
    """Update User via API."""
    # Auth setup
    user_data = {
        'email': 'qzS5V@enrzw.com',
        'last_name': 'UyCBC',
        'password': 'VxIzx',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    user_data = {
        'email': '6UJ8G@wjras.com',
        'first_name': 'GbC64',
        'last_name': 'z99on',
        'password': 'lBjjs',
        'is_superuser': True,
        'picture': 'ZeuYO',
        'is_active': True,
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

    resp_c = client.post('/api/v1/users/', json=user_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = []

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in user_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/users/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['email'] == update_data['email']
    assert updated['first_name'] == update_data['first_name']
    assert updated['last_name'] == update_data['last_name']
    assert updated['is_superuser'] == update_data['is_superuser']
    assert updated['picture'] == update_data['picture']
    assert updated['is_active'] == update_data['is_active']


def test_get_user_api(client, db):
    """Get User via API."""
    # Auth setup
    user_data = {
        'email': '0NN0N@x84ui.com',
        'last_name': 'zniZb',
        'password': '21Tdv',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    user_data = {
        'email': 'vajIM@3r6xv.com',
        'first_name': 'T33yd',
        'last_name': 'WGSrT',
        'password': 'saQJO',
        'is_superuser': False,
        'picture': 'JLyP1',
        'is_active': False,
    }

    client.post('/api/v1/users/', json=user_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/users/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_user_api(client, db):
    """Get_by_id User via API."""
    # Auth setup
    user_data = {
        'email': 'gHKZf@sfj9z.com',
        'last_name': 'EGrSm',
        'password': 'NIADz',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    user_data = {
        'email': 'f5aTN@7skne.com',
        'first_name': 'TMuxY',
        'last_name': 'oxI9M',
        'password': 'v2b3O',
        'is_superuser': False,
        'picture': '73eLr',
        'is_active': False,
    }

    resp_c = client.post('/api/v1/users/', json=user_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/users/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_user_api(client, db):
    """Delete User via API."""
    # Auth setup
    user_data = {
        'email': 'VIZ7U@n2jam.com',
        'last_name': 'TgzoF',
        'password': 'yOpiM',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    user_data = {
        'email': 'cQr3Z@e4ft5.com',
        'first_name': 'zEW4b',
        'last_name': 'U5dxi',
        'password': 'lHlny',
        'is_superuser': True,
        'picture': 'r3cCh',
        'is_active': True,
    }

    resp_c = client.post('/api/v1/users/', json=user_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/users/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'User deleted successfully'
    resp_chk = client.get(f'/api/v1/users/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND


def test_create_user_with_roles_api(client, db):
    """Ensure creating a user persists role assignments."""
    suffix = random.randint(1, 10000)
    admin_data = {
        'email': f'admin_roles_{suffix}@scolary.com',
        'last_name': 'Admin',
        'password': 'Secret1',
        'is_superuser': True,
        'is_active': True,
    }
    admin = crud.user.create(db, obj_in=schemas.UserCreate(**admin_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(admin.id), 'email': admin.email})

    role_ids = []
    for idx in range(2):
        role = crud.role.create(
            db=db,
            obj_in=schemas.RoleCreate(name=f'Role_{idx}_{random.randint(1, 10000)}'),
        )
        role_ids.append(role.id)

    mention_ids = []
    for idx in range(2):
        mention = crud.mention.create(
            db=db,
            obj_in=schemas.MentionCreate(
                name=f'Mention_{idx}_{random.randint(1, 10000)}',
                slug=f'mention_{idx}_{random.randint(1, 10000)}',
                abbreviation=f'M{idx}',
                plugged='plug',
                background='bg',
            ),
        )
        mention_ids.append(mention.id)

    user_payload = {
        'email': f'roles_user_{suffix}@scolary.com',
        'first_name': 'Role',
        'last_name': 'Tester',
        'password': 'Secure1',
        'is_superuser': False,
        'picture': 'pic.png',
        'is_active': True,
        'role_ids': role_ids,
        'mention_ids': mention_ids,
    }

    resp = client.post('/api/v1/users/', json=user_payload, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()

    assigned_roles = [
        ur.id_role
        for ur in db.query(UserRole)
        .filter(UserRole.id_user == created['id'])
        .all()
    ]
    assert sorted(assigned_roles) == sorted(role_ids)

    assigned_mentions = [
        um.id_mention
        for um in db.query(UserMention)
        .filter(UserMention.id_user == created['id'])
        .all()
    ]
    assert sorted(assigned_mentions) == sorted(mention_ids)


def test_update_user_roles_api(client, db):
    """Ensure updating a user synchronizes role assignments."""
    suffix = random.randint(1, 10000)
    admin_data = {
        'email': f'admin_roles_update_{suffix}@scolary.com',
        'last_name': 'Admin',
        'password': 'Secret1',
        'is_superuser': True,
        'is_active': True,
    }
    admin = crud.user.create(db, obj_in=schemas.UserCreate(**admin_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(admin.id), 'email': admin.email})

    roles = []
    for idx in range(3):
        role = crud.role.create(
            db=db,
            obj_in=schemas.RoleCreate(name=f'Role_up_{idx}_{random.randint(1, 10000)}'),
        )
        roles.append(role.id)

    mentions = []
    for idx in range(3):
        mention = crud.mention.create(
            db=db,
            obj_in=schemas.MentionCreate(
                name=f'Mention_up_{idx}_{random.randint(1, 10000)}',
                slug=f'mention-up-{idx}-{random.randint(1, 10000)}',
                abbreviation=f'M{idx}',
                plugged='plug',
                background='bg',
            ),
        )
        mentions.append(mention.id)

    create_payload = {
        'email': f'roles_update_{suffix}@scolary.com',
        'first_name': 'Role',
        'last_name': 'Switcher',
        'password': 'Secure1',
        'is_superuser': False,
        'picture': 'pic.png',
        'is_active': True,
        'role_ids': roles[:2],
        'mention_ids': mentions[:2],
    }

    resp_create = client.post('/api/v1/users/', json=create_payload, headers={"Authorization": f"Bearer {token}"})
    assert resp_create.status_code == status.HTTP_200_OK, resp_create.text
    created_user = resp_create.json()

    update_payload = {
        'role_ids': roles[1:],
        'mention_ids': mentions[1:],
        'first_name': 'RoleUpdated',
    }

    resp_update = client.put(
        f'/api/v1/users/{created_user["id"]}',
        json=update_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_update.status_code == status.HTTP_200_OK, resp_update.text

    assigned_roles = sorted(
        [
            ur.id_role
            for ur in db.query(UserRole).filter(UserRole.id_user == created_user['id']).all()
        ]
    )
    assert assigned_roles == sorted(roles[1:])

    assigned_mentions = sorted(
        [
            um.id_mention
            for um in db.query(UserMention).filter(UserMention.id_user == created_user['id']).all()
        ]
    )
    assert assigned_mentions == sorted(mentions[1:])


def test_upload_user_picture_api(client, db):
    """Upload and persist a profile picture."""
    suffix = random.randint(1, 10000)
    admin_data = {
        'email': f'admin_upload_{suffix}@scolary.com',
        'last_name': 'Admin',
        'password': 'Secret1',
        'is_superuser': True,
        'is_active': True,
    }
    admin = crud.user.create(db, obj_in=schemas.UserCreate(**admin_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(admin.id), 'email': admin.email})

    user_payload = {
        'email': f'upload_user_{suffix}@scolary.com',
        'first_name': 'Pic',
        'last_name': 'Target',
        'password': 'Secure1',
        'is_superuser': False,
        'picture': None,
        'is_active': True,
    }
    resp_create = client.post('/api/v1/users/', json=user_payload, headers={"Authorization": f"Bearer {token}"})
    user_id = resp_create.json()['id']

    file_bytes = BytesIO(b'\x89PNG\r\n\x1a\nfakeimagedata')
    resp_upload = client.post(
        f'/api/v1/users/{user_id}/picture',
        headers={"Authorization": f"Bearer {token}"},
        files={'file': ('avatar.png', file_bytes, 'image/png')},
    )
    assert resp_upload.status_code == status.HTTP_200_OK, resp_upload.text
    uploaded = resp_upload.json()
    assert uploaded['picture'].startswith('/files/user_pictures/')
    stored_path = Path(uploaded['picture'].lstrip('/'))
    assert stored_path.exists()
    stored_path.unlink(missing_ok=True)


def test_upload_user_picture_invalid_type_api(client, db):
    """Reject uploads with unsupported mimetype."""
    suffix = random.randint(1, 10000)
    admin_data = {
        'email': f'admin_upload_invalid_{suffix}@scolary.com',
        'last_name': 'Admin',
        'password': 'Secret1',
        'is_superuser': True,
        'is_active': True,
    }
    admin = crud.user.create(db, obj_in=schemas.UserCreate(**admin_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(admin.id), 'email': admin.email})

    user_payload = {
        'email': f'upload_invalid_{suffix}@scolary.com',
        'first_name': 'Pic',
        'last_name': 'Target',
        'password': 'Secure1',
        'is_superuser': False,
        'picture': None,
        'is_active': True,
    }
    resp_create = client.post('/api/v1/users/', json=user_payload, headers={"Authorization": f"Bearer {token}"})
    user_id = resp_create.json()['id']

    resp_upload = client.post(
        f'/api/v1/users/{user_id}/picture',
        headers={"Authorization": f"Bearer {token}"},
        files={'file': ('avatar.txt', BytesIO(b'not image'), 'text/plain')},
    )
    assert resp_upload.status_code == status.HTTP_400_BAD_REQUEST

# begin #
# ---write your code here--- #
# end #
