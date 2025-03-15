from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.responses import Responses
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationShortDB, DonationDB
from app.services.investing import process_investment_for_donation

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
    responses={**Responses.Errors.UNAUTHORIZED,
               **Responses.Errors.FORBIDDEN}
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров.

    Возвращает список всех пожертвований."""
    return await donation_crud.get_all(session)


@router.post(
    '/',
    response_model=DonationShortDB,
    response_model_exclude_none=True,
    responses={**Responses.Errors.UNAUTHORIZED}
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(donation, session, user)
    return await process_investment_for_donation(new_donation, session)


@router.get(
    '/my',
    response_model=list[DonationShortDB],
    responses={**Responses.Errors.UNAUTHORIZED}
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    return await donation_crud.get_by_attribute(
        'user_id', user.id, session
    )
