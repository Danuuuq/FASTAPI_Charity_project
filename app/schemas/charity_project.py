from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field

from app.core.config import settings


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(max_length=settings.MAX_LENGTH_NAME)
    description: Optional[str] = Field()
    full_amount: Optional[int] = Field(gt=settings.GT_FOR_AMOUNT)

    class Config:
        extra = Extra.forbid
        min_anystr_length = settings.MIN_LENGTH_NAME


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(max_length=settings.MAX_LENGTH_NAME)
    description: str = Field()
    full_amount: int = Field(gt=settings.GT_FOR_AMOUNT)

    class Config:
        min_anystr_length = settings.MIN_LENGTH_NAME


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectClose(BaseModel):
    project_name: str
    time_close: float
    project_description: str
