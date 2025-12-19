from typing import Optional, List, Any, Dict

from pydantic import BaseModel, ConfigDict

from app.enum.card_type import CardTypeEnum
from .mention import Mention
from .journey import Journey


class CardBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    card_type: Optional[CardTypeEnum] = None
    html_template: Optional[str] = None
    css_styles: Optional[str] = None
    id_mention: Optional[int] = None
    id_journey: Optional[int] = None


class CardCreate(CardBase):
    name: str
    card_type: CardTypeEnum
    html_template: str


class CardUpdate(CardBase):
    pass


class CardInDBBase(CardBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Card(CardInDBBase):
    pass


class CardWithRelation(CardInDBBase):
    mention: Optional[Mention] = None
    journey: Optional[Journey] = None


class CardInDB(CardInDBBase):
    pass


class ResponseCard(BaseModel):
    count: int
    data: Optional[List[CardWithRelation]]


class CardRenderRequest(BaseModel):
    data: Optional[Dict[str, Any]] = None


class CardPdfRenderRequest(BaseModel):
    html_template: str
    css_styles: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    copies: Optional[int] = 1
    page_size: Optional[str] = "A4"
