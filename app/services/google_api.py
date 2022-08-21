from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject

FORMAT = '%Y/%m/%d %H:%M:%S'
DOCUMENT_TITLE = 'Отчет на {0}'
LIST_TITLE = 'Лист1'
SHEET_TYPE = 'GRID'
DIMENTIONS = (100, 11)
LANG = 'ru_RU'
TABLE_HEADER = [
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheet_create(wrapper_services: Aiogoogle) -> str:
    now = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': DOCUMENT_TITLE.format(now),
                       'locale': LANG},
        'sheets': [{'properties': {'sheetType': SHEET_TYPE,
                                   'sheetId': 0,
                                   'title': LIST_TITLE,
                                   'gridProperties': {'rowCount': DIMENTIONS[0],
                                                      'columnCount': DIMENTIONS[1]}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_service: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_service.discover('drive', 'v3')
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: List[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [['Отчет от', now_date_time]] + TABLE_HEADER
    for proj in projects:
        name = proj.name
        duration = str(proj.close_date - proj.create_date)
        desc = proj.description
        new_row = [name, duration, desc]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )