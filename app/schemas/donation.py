from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationCreate(BaseModel):
    comment: Optional[str]
    full_amount: int = Field(..., gt=0, example=100)


class DonationDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class ExtendedDonationDB(DonationDB):
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    user_id: int
