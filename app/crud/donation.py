from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):

    async def get_with_amount_donations(
        self,
        session: AsyncSession
    ) -> Optional[Donation]:
        donation = await session.execute(
            select(self.model).where(
                self.model.full_amount > self.model.invested_amount
            ).with_for_update()
        )
        return donation.scalars()


donation_crud = CRUDDonation(Donation)
