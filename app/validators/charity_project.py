from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.charity_project import charity_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def get_close_project_or_404(session: AsyncSession):
    projects = await charity_crud.get_projects_by_completion_rate(session)
    if not projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Нет закрытых проектов")
    return projects


async def get_or_404(
    obj_id: int,
    session: AsyncSession
) -> CharityProject:
    """Проверка на наличие проекта в базе данных.

    Если проект отсутствует возвращается ошибка 404,
    в противном случае возвращается объект проекта."""
    db_obj = await charity_crud.get(obj_id, session)
    if db_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Проекта с id: {obj_id} отсутствует'
        )
    return db_obj


async def check_duplicate_name(
    project_name: str,
    session: AsyncSession
) -> None:
    """Проверка на уникальность имени проекта.

    Если имя не уникальное возвращается ошибка 422"""
    project = await charity_crud.get_obj_by_name(
        project_name, session
    )
    if project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_invested_project(
    project: CharityProject,
) -> None:
    """Проверка что в проекте не инвестировали.

    Если в проект были внесены инвестиции или он закрыт его нельзя удалить"""
    if (project.invested_amount > settings.DEFAULT_AMOUNT or
            project.fully_invested):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def validation_update_project(
    org_project: CharityProject,
    upd_project: CharityProjectUpdate,
    session: AsyncSession
) -> None:
    """Проверка объекта перед обновление.

    Закрытый проект нельзя редактировать.
    Нельзя установить сумму меньше вложенной.
    Нельзя изменить на имя, которое уже есть в БД."""
    if org_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=('Закрытый проект нельзя редактировать!')
        )
    if (upd_project.full_amount and
       (org_project.invested_amount > upd_project.full_amount)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=('Нельзя установить значение full_amount'
                    'меньше уже вложенной суммы.')
        )
    if upd_project.name:
        await check_duplicate_name(upd_project.name, session)
