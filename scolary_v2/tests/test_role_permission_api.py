# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_role_permission_api(client, db):
    """Create RolePermission via API."""
    # Auth setup
    user_data = {
        'email': 'mq4up@qfvit.com',
        'last_name': 'PkO1c',
        'password': 'Wi6Ut',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='icDb9',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='Vswfz',
        method='B5JNk',
        model_name='OljBZ',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

    role_permission_data = {
        'id_role': role.id,
        'id_permission': permission.id,
    }

    resp = client.post('/api/v1/role_permissions/', json=role_permission_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_role'] == role_permission_data['id_role']
    assert created['id_permission'] == role_permission_data['id_permission']


def test_update_role_permission_api(client, db):
    """Update RolePermission via API."""
    # Auth setup
    user_data = {
        'email': 'grlWJ@rdqtx.com',
        'last_name': 'rTCl4',
        'password': 'eRr4U',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='bNru7',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='Vc47u',
        method='UYsTU',
        model_name='DZRxz',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

    role_permission_data = {
        'id_role': role.id,
        'id_permission': permission.id,
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

    resp_c = client.post('/api/v1/role_permissions/', json=role_permission_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_role', 'id_permission']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in role_permission_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/role_permissions/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']


def test_get_role_permission_api(client, db):
    """Get RolePermission via API."""
    # Auth setup
    user_data = {
        'email': 'tmmU1@erscu.com',
        'last_name': 'tzvQR',
        'password': '6cg8l',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='7YHpp',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='Vf0pg',
        method='9NuVN',
        model_name='jSNBy',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

    role_permission_data = {
        'id_role': role.id,
        'id_permission': permission.id,
    }

    client.post('/api/v1/role_permissions/', json=role_permission_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/role_permissions/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_role_permission_api(client, db):
    """Get_by_id RolePermission via API."""
    # Auth setup
    user_data = {
        'email': '2LvRV@duyfb.com',
        'last_name': 'LCIxD',
        'password': 'XEol3',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='woXBT',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='aM3ME',
        method='waAD0',
        model_name='cvSo1',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

    role_permission_data = {
        'id_role': role.id,
        'id_permission': permission.id,
    }

    resp_c = client.post('/api/v1/role_permissions/', json=role_permission_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/role_permissions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_role_permission_api(client, db):
    """Delete RolePermission via API."""
    # Auth setup
    user_data = {
        'email': 'wV0Mn@0ln8g.com',
        'last_name': 'rtQqj',
        'password': 'fAEGN',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='oi4qW',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='2Fmga',
        method='mTLI2',
        model_name='TPUjn',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

    role_permission_data = {
        'id_role': role.id,
        'id_permission': permission.id,
    }

    resp_c = client.post('/api/v1/role_permissions/', json=role_permission_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/role_permissions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'RolePermission deleted successfully'
    resp_chk = client.get(f'/api/v1/role_permissions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #
