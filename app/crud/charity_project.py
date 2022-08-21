# flake8: noqa: E712
from datetime import datetime
from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> List[CharityProject]:
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == True
            )
        )
        projects: List[CharityProject] = projects.scalars().all()
        projects.sort(key=lambda x: x.close_date - x.create_date)

        return projects

    async def update(
            self,
            project: CharityProject,
            obj_in: CharityProjectUpdate,
            session: AsyncSession
    ):
        obj_data = jsonable_encoder(project)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(project, field, update_data[field])
        if project.invested_amount == project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project

    async def remove(
            self,
            project,
            session: AsyncSession,
    ):
        await session.delete(project)
        await session.commit()
        return project


charity_project_crud = CRUDCharityProject(CharityProject)
