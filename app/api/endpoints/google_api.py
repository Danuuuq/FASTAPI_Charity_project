from aiogoogle import Aiogoogle
from aiogoogle.excs import AiogoogleError
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.services.google_api import generate_spreadsheet_report
from app.schemas.charity_project import CharityProjectClose
from app.validators.charity_project import get_close_project_or_404

router = APIRouter()


@router.post('/', response_model=list[CharityProjectClose])
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service),
):
    projects = await get_close_project_or_404(session)
    try:
        await generate_spreadsheet_report(projects, wrapper_service)
    except AiogoogleError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при создании таблицы, сообщите администратору')
    return projects
