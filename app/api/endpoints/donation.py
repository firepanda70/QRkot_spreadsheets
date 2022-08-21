from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate, DonationDB, ExtendedDonationDB
)
from app.services import invest_donation

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def donate(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """
    Отправка нового прожертвования.

    Доступно только для авторизованных пользователей.
    """
    new_donation = await donation_crud.create(
        donation, session, user
    )
    new_donation = await invest_donation(new_donation, session)
    return new_donation


@router.get(
    '/',
    response_model=List[ExtendedDonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Возвращает список всех пожертвований.

    Доступно только для суперюзеров.
    """
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=List[DonationDB],
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """
    Возвращает список всех собственных пожертвований.

    Доступно только для авторизованных пользователей.
    """
    donations = await donation_crud.get_by_user(user, session)
    return donations
