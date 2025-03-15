from datetime import datetime, timedelta, timezone

from aiogoogle import Aiogoogle
from aiogoogle.resource import Resource

from app.core.config import settings
from app.models.charity_project import CharityProject


async def spreadsheets_create(
    wrapper_service: Aiogoogle,
    now_date_time: str,
    service: Resource
) -> str:
    spreadsheets_body = {
        'properties': {'title': f'Отчет на {now_date_time}',
                       'locale': settings.LOCALE},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {
                                       'rowCount': settings.ROW_SHEETS,
                                       'columnCount': settings.COLUMN_SHEETS
                                   }}}]
    }
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=spreadsheets_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle,
    service: Resource
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheetid: str,
    projects: list[CharityProject],
    wrapper_services: Aiogoogle,
    now_date_time: str,
    service: Resource
) -> None:
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        new_row = [str(project['project_name']),
                   str(timedelta(project['time_close'])),
                   str(project['project_description'])]
        table_values.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:C{len(table_values)}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )


async def generate_spreadsheet_report(
    projects: list[CharityProject],
    wrapper_service: Aiogoogle
) -> None:
    now_date_time = datetime.now(timezone.utc).strftime(settings.FORMAT_DATE)
    sheet_service = await wrapper_service.discover('sheets', 'v4')
    drive_service = await wrapper_service.discover('drive', 'v3')
    spreadsheetid = await spreadsheets_create(wrapper_service, now_date_time,
                                              sheet_service)
    await set_user_permissions(spreadsheetid, wrapper_service, drive_service)
    await spreadsheets_update_value(spreadsheetid, projects, wrapper_service,
                                    now_date_time, sheet_service)
