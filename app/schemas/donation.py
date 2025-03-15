from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field

from app.core.config import settings


class DonationBase(BaseModel):
    full_amount: int = Field(gt=settings.GT_FOR_AMOUNT)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationShortDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationShortDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
