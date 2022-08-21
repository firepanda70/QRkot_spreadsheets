from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
# Ради статус-кодов устанавливать весь джанго мне показалось избыточным
from app.misc import status


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Благотворительный проект не найден'
        )
    return project


async def check_is_not_closed(
        project: CharityProject,
        session: AsyncSession,
) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_valid_full_amount(
        project: CharityProject,
        value: int,
        session: AsyncSession,
) -> None:
    if project.invested_amount > value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Невозможно сделать требуемую сумму для проекта меньше, чем уже было проинветстированно'
        )


async def check_have_no_investments(
        project: CharityProject,
        session: AsyncSession,
):
    if project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
