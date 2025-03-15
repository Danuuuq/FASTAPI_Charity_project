from datetime import datetime, timezone
from typing import Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import commit_change
from app.models import User


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_all(
        self,
        session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user:
            obj_in_data['user_id'] = user.id
        obj_in_data['invested_amount'] = settings.DEFAULT_AMOUNT
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        session: AsyncSession,
        obj_in=None
    ):
        if obj_in is not None:
            update_data = obj_in.dict(exclude_unset=True)
        else:
            update_data = db_obj.__dict__

        obj_data = jsonable_encoder(db_obj)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if db_obj.full_amount == db_obj.invested_amount:
            db_obj.close_date = datetime.now(timezone.utc)
            db_obj.fully_invested = True
        session.add(db_obj)
        return db_obj

    async def bulk_update(
        self,
        db_objs,
        session: AsyncSession,
    ) -> None:
        for db_obj in db_objs:
            await self.update(db_obj, session)

    async def delete(
        self,
        db_obj,
        session: AsyncSession
    ):
        await session.delete(db_obj)
        await commit_change(session)
        return db_obj

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: Union[str, int],
        session: AsyncSession
    ):
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().all()
