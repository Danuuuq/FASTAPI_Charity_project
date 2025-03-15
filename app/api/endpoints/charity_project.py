from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.responses import Responses
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.investing import process_investment_for_project
from app.validators.charity_project import (
    validation_update_project, check_duplicate_name,
    check_invested_project, get_or_404
)


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session)
) -> list[CharityProjectDB]:
    """Возвращает список всех проектов."""
    return await charity_crud.get_all(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    responses={**Responses.Errors.NOT_UNIQUE_NAME,
               **Responses.Errors.UNAUTHORIZED,
               **Responses.Errors.FORBIDDEN}
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Только для супер пользователей.

    Создаёт благотворительный проект."""
    await check_duplicate_name(charity_project.name, session)
    new_project = await charity_crud.create(charity_project, session)
    return await process_investment_for_project(new_project, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    responses={**Responses.Errors.PROJECT_CLOSED_OR_WITH_DONATIONS,
               **Responses.Errors.UNAUTHORIZED,
               **Responses.Errors.FORBIDDEN}
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Только для супер пользователей.

    Удаляет проект. Нельзя удалить проект, в который уже были
    инвестированы средства, его можно только закрыть."""
    project = await get_or_404(project_id, session)
    await check_invested_project(project)
    return await charity_crud.delete(project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    responses={**Responses.Errors.INVALID_OPERATION,
               **Responses.Errors.UNAUTHORIZED,
               **Responses.Errors.FORBIDDEN}
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Только для супер пользователей.

    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной."""
    project = await get_or_404(project_id, session)
    await validation_update_project(project, obj_in, session)
    upd_project = await charity_crud.update(project, session, obj_in)
    return await process_investment_for_project(upd_project, session)
