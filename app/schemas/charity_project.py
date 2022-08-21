from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class CharityProjectCreate(BaseModel):
    full_amount: int = Field(..., gt=0, example=200)
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(BaseModel):
    full_amount: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
