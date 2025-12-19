# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.user import User
from app.models.user_role import UserRole
from app.models.user_mention import UserMention
from app.schemas.user import UserCreate, UserUpdate

from app.core.security import get_password_hash, verify_password
from fastapi.encoders import jsonable_encoder

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[User]:
        return db.query(User).filter(getattr(User, field) == value).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def is_superuser(self, user: User) -> User:
        return user.is_superuser

    def is_active(self, user: User) -> User:
        return user.is_active

    def authenticate(self, db: Session, *, email: str, password: str) -> User:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def _normalize_relation_ids(self, ids: Optional[List[int]]) -> List[int]:
        if not ids:
            return []
        normalized = []
        for value in ids:
            if value is None:
                continue
            try:
                normalized.append(int(value))
            except (TypeError, ValueError):
                continue
        # Preserve order while removing duplicates
        return list(dict.fromkeys(normalized))

    def _sync_user_roles(
        self,
        db: Session,
        *,
        user_id: int,
        role_ids: Optional[List[int]],
        commit: bool = True,
    ) -> None:
        target_ids = set(self._normalize_relation_ids(role_ids))
        if not target_ids and role_ids is None:
            return

        existing_roles = db.query(UserRole).filter(UserRole.id_user == user_id).all()
        existing_ids = {ur.id_role for ur in existing_roles}

        for user_role in existing_roles:
            if user_role.id_role not in target_ids:
                db.delete(user_role)

        for role_id in target_ids - existing_ids:
            db.add(UserRole(id_user=user_id, id_role=role_id))

        if commit:
            db.commit()

    def _sync_user_mentions(
        self,
        db: Session,
        *,
        user_id: int,
        mention_ids: Optional[List[int]],
        commit: bool = True,
    ) -> None:
        target_ids = set(self._normalize_relation_ids(mention_ids))
        if not target_ids and mention_ids is None:
            return

        existing_mentions = db.query(UserMention).filter(UserMention.id_user == user_id).all()
        existing_ids = {um.id_mention for um in existing_mentions}

        for user_mention in existing_mentions:
            if user_mention.id_mention not in target_ids:
                db.delete(user_mention)

        for mention_id in target_ids - existing_ids:
            db.add(UserMention(id_user=user_id, id_mention=mention_id))

        if commit:
            db.commit()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        obj_data = jsonable_encoder(obj_in)
        role_ids = obj_data.pop('role_ids', None)
        mention_ids = obj_data.pop('mention_ids', None)
        pass_value = obj_data.pop('password')
        db_obj = User(hashed_password=get_password_hash(pass_value), **obj_data)
        db.add(db_obj)
        db.flush()
        self._sync_user_roles(db, user_id=db_obj.id, role_ids=role_ids, commit=False)
        self._sync_user_mentions(db, user_id=db_obj.id, mention_ids=mention_ids, commit=False)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]],
        commit: bool = True,
    ) -> User:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in.copy()
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        role_ids = update_data.pop('role_ids', None)
        mention_ids = update_data.pop('mention_ids', None)
        update_data["updated_at"] = func.now()

        password_value = update_data.pop("password", None)
        if password_value:
            update_data["hashed_password"] = get_password_hash(password_value)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.flush()
        self._sync_user_roles(db, user_id=db_obj.id, role_ids=role_ids, commit=False)
        self._sync_user_mentions(db, user_id=db_obj.id, mention_ids=mention_ids, commit=False)
        if commit:
            db.commit()
            db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)


# begin #
# ---write your code here--- #
# end #
