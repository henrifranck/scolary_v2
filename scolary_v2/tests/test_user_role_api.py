# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_user_role_api(client, db):
    """Create UserRole via API."""
    # Auth setup
    user_data = {
        'email': 'x4BE8@zsipn.com',
        'last_name': 'OhgqL',
        'password': '134Qk',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for User
    user_data = schemas.UserCreate(
        email='hGqEq@anvcw.com',
        first_name='1K0f5',
        last_name='tiGCm',
        password='J53rZ',
        is_superuser=True,
        picture='1zEdo',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='FkAeQ',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    user_role_data = {
        'id_user': user.id,
        'id_role': role.id,
    }

    resp = client.post('/api/v1/user_roles/', json=user_role_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_user'] == user_role_data['id_user']
    assert created['id_role'] == user_role_data['id_role']


def test_update_user_role_api(client, db):
    """Update UserRole via API."""
    # Auth setup
    user_data = {
        'email': 'tnwPK@mabku.com',
        'last_name': 'flKhV',
        'password': 'YYsNt',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for User
    user_data = schemas.UserCreate(
        email='rNJns@zbwan.com',
        first_name='jE032',
        last_name='5pZv5',
        password='nfQHv',
        is_superuser=False,
        picture='oMAXr',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='eDlPc',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    user_role_data = {
        'id_user': user.id,
        'id_role': role.id,
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

    resp_c = client.post('/api/v1/user_roles/', json=user_role_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_user', 'id_role']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in user_role_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/user_roles/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']


def test_get_user_role_api(client, db):
    """Get UserRole via API."""
    # Auth setup
    user_data = {
        'email': 'XElU1@zqceb.com',
        'last_name': 'efhQD',
        'password': 'yOVb3',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for User
    user_data = schemas.UserCreate(
        email='2g9Km@7po9v.com',
        first_name='ahBDl',
        last_name='HVXii',
        password='kuvcy',
        is_superuser=True,
        picture='AqBTe',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='ZBM8n',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    user_role_data = {
        'id_user': user.id,
        'id_role': role.id,
    }

    client.post('/api/v1/user_roles/', json=user_role_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/user_roles/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_user_role_api(client, db):
    """Get_by_id UserRole via API."""
    # Auth setup
    user_data = {
        'email': 'IFULo@vxv99.com',
        'last_name': 'UFIl6',
        'password': 'drqrM',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for User
    user_data = schemas.UserCreate(
        email='FrFMD@1nyqt.com',
        first_name='kRmM6',
        last_name='ySlL8',
        password='xVxuC',
        is_superuser=False,
        picture='Q2idc',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='IRsPV',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    user_role_data = {
        'id_user': user.id,
        'id_role': role.id,
    }

    resp_c = client.post('/api/v1/user_roles/', json=user_role_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/user_roles/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_user_role_api(client, db):
    """Delete UserRole via API."""
    # Auth setup
    user_data = {
        'email': 'vgKjt@x1tgq.com',
        'last_name': 'HAJ5I',
        'password': 'FqYE0',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for User
    user_data = schemas.UserCreate(
        email='UMnqU@lyjvw.com',
        first_name='qela8',
        last_name='vAtV6',
        password='iDI5E',
        is_superuser=True,
        picture='tb07A',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='INByv',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    user_role_data = {
        'id_user': user.id,
        'id_role': role.id,
    }

    resp_c = client.post('/api/v1/user_roles/', json=user_role_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/user_roles/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'UserRole deleted successfully'
    resp_chk = client.get(f'/api/v1/user_roles/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #
