from typing import Dict

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends

from app.schemas.google_api import GoogleAPIStringResponseSchema
from app.core import db, user
from app.core.google_client import get_service
from app.crud.charity_project import charity_project_crud
from app.services import google_api as go_service

router = APIRouter()


@router.get(
    path='/',
    response_model=GoogleAPIStringResponseSchema,
    dependencies=[Depends(user.current_superuser)]
)
async def get_report(
    session: db.AsyncSession = Depends(db.get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service),
) -> Dict[str, str]:
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )

    spreadsheet_id = await go_service.get_spreadsheet_id(
        wrapper_service=wrapper_service
    )

    await go_service.spreadsheet_update_value(
        spreadsheet_id=spreadsheet_id,
        projects=projects,
        wrapper_service=wrapper_service
    )
    return {'url': f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'}
