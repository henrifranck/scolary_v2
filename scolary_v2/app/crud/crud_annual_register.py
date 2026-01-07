# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any, cast

from sqlalchemy import func, Integer
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import RegisterSemester
from app.models.annual_register import AnnualRegister
from app.schemas.annual_register import AnnualRegisterCreate, AnnualRegisterUpdate
from app.enum.register_type import RegisterTypeEnum
import secrets
import string


class CRUDAnnualRegister(CRUDBase[AnnualRegister, AnnualRegisterCreate, AnnualRegisterUpdate]):
    @staticmethod
    def _generate_registration_code(length: int = 8) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def create(
            self,
            db: Session,
            *,
            obj_in: AnnualRegisterCreate,
            user_id: int = None,
            commit: bool = True,
            refresh: bool = True
    ) -> AnnualRegister:
        data = obj_in.model_dump()
        if (
            data.get("register_type") == RegisterTypeEnum.REGISTRATION.value
        ):
            data["registration_code"] = self._generate_registration_code()
        db_obj = (
            self.model(**data)
            if not user_id
            else self.model(**data, last_user_to_interact=user_id)
        )
        db.add(db_obj)
        if commit:
            db.commit()
        if refresh:
            db.refresh(db_obj)
        return db_obj

    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[AnnualRegister]:
        return db.query(AnnualRegister).filter(getattr(AnnualRegister, field) == value).first()


annual_register = CRUDAnnualRegister(AnnualRegister)

# begin #
# ---write your code here--- #
# end #
