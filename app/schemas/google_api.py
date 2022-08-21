from typing import Dict, List

from pydantic import BaseModel, Extra, Field, HttpUrl


class GoogleAPIBaseSchema(BaseModel):
    ptojects: List[Dict[str, str]] = Field(
        ...,
        example=[
            {
                'name': 'Для помощи белым котам',
                'time_spent': '1 day, 12:27:54.123456',
                'description': 'Будем из одиноких белых котов делать других'
            }
        ]
    )

    class Config:
        extra = Extra.forbid


class GoogleAPIStringResponseSchema(BaseModel):
    url: HttpUrl = Field(
        ...,
        example='https://docs.google.com/spreadsheets/d/spreadsheet_id'
    )
