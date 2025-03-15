from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.core.config import settings
from app.models.charity_project import CharityProject


class CRUDCharity(CRUDBase):

    async def get_obj_by_name(
        self,
        name: str,
        session: AsyncSession
    ) -> Optional[CharityProject]:
        object = await session.execute(
            select(self.model).where(
                self.model.name == name
            )
        )
        return object.scalars().first()

    async def get_project_for_invest(
        self,
        session: AsyncSession
    ) -> Optional[CharityProject]:
        projects = await session.execute(
            select(self.model).where(
                self.model.fully_invested == settings.DEFAULT_AMOUNT
            ).with_for_update()
        )
        return projects.scalars()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> Optional[CharityProject]:
        projects = await session.execute(
            select(self.model.name.label('project_name'),
                   (func.julianday(self.model.close_date) -
                    func.julianday(self.model.create_date))
                   .label('time_close'),
                   self.model.description.label('project_description')).where(
                self.model.fully_invested == 1
            ).order_by(func.julianday(self.model.close_date) -
                       func.julianday(self.model.create_date))
        )
        return projects.all()


charity_crud = CRUDCharity(CharityProject)
