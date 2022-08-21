# flake8: noqa: E712
from datetime import datetime
from typing import Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, CharityProject


async def invest_all_free_donations(
    proj: CharityProject,
    session: AsyncSession
) -> CharityProject:
    to_invest = await session.execute(
        select(Donation).where(
            Donation.fully_invested == False
        ).order_by(Donation.create_date)
    )
    to_invest: list[Donation] = to_invest.scalars().all()
    i = 0
    donation = None

    while not proj.fully_invested and len(to_invest) > i:
        donation = to_invest[i]
        proj, donation = await count_investment(proj, donation, session)
        i += 1

    session.add(proj)
    if donation:
        session.add(donation)
    await session.commit()
    await session.refresh(proj)
    return proj


async def invest_donation(
    donation: Donation,
    session: AsyncSession
) -> Donation:
    unf_proj = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == False
        ).order_by(CharityProject.create_date)
    )
    unf_proj: list[CharityProject] = unf_proj.scalars().all()
    proj = None
    i = 0

    while not donation.fully_invested and len(unf_proj) > i:
        proj = unf_proj[i]
        proj, donation = await count_investment(proj, donation, session)
        i += 1

    if proj:
        session.add(proj)
    session.add(donation)
    await session.commit()
    await session.refresh(donation)
    return donation


async def count_investment(
    proj: CharityProject,
    donation: Donation,
    session: AsyncSession
) -> Tuple[CharityProject, Donation]:

    need = proj.full_amount - proj.invested_amount
    spare = donation.full_amount - donation.invested_amount
    if need <= spare:
        proj.invested_amount = proj.full_amount
        proj.fully_invested = True
        proj.close_date = datetime.now()
        session.add(proj)
        donation.invested_amount += need
        if donation.invested_amount == donation.full_amount:
            donation.fully_invested = True
            donation.close_date = datetime.now()
            session.add(donation)
    else:
        proj.invested_amount += spare
        donation.invested_amount = donation.full_amount
        donation.fully_invested = True
        donation.close_date = datetime.now()
        session.add(donation)
    return proj, donation
