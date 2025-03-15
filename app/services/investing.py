from typing import Union, Iterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import commit_change
from app.crud.charity_project import charity_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def process_investment_for_project(
    project: CharityProject,
    session: AsyncSession
) -> CharityProject:
    donations = await donation_crud.get_with_amount_donations(session)
    upd_project, upd_donations = invest_in_project(project, donations)
    await donation_crud.bulk_update(upd_donations, session)
    await charity_crud.update(upd_project, session)
    return await commit_change(session, upd_project)


async def process_investment_for_donation(
    donation: Donation,
    session: AsyncSession
) -> Donation:
    projects = await charity_crud.get_project_for_invest(session)
    upd_donation, upd_projects = invest_in_project(donation, projects)
    await donation_crud.bulk_update(upd_projects, session)
    await charity_crud.update(upd_donation, session)
    return await commit_change(session, upd_donation)


def invest_in_project(
    target: Union[CharityProject, Donation],
    sources: Iterator[Union[CharityProject, Donation]],
) -> tuple[CharityProject, list[Donation]]:
    """Инвестирование средств в проекты.

    В зависимости от входных данных происходит распределение свободных средств.
    input_object: проект или донат"""
    upd_sources = []
    for source in sources:
        if target.invested_amount == target.full_amount:
            break
        target_amount = target.full_amount - target.invested_amount
        available_amount = (source.full_amount -
                            source.invested_amount)
        investment_use = min(target_amount, available_amount)
        source.invested_amount += investment_use
        target.invested_amount += investment_use
        upd_sources.append(source)
    return target, upd_sources
