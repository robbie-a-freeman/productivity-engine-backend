from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime


class TaskSchema(BaseModel):
    name: str = Field(...)
    last_completion: datetime = Field(...)
    days_between_completions: float = Field(...)
    creation_date: datetime = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Vacuum the living room",
                "last_completion": "2032-04-23T10:20:30.400+02:30",
                "days_between_completions": 14.0,
                "creation_date": "2032-04-23T10:20:30.400+02:30"
            }
        }


class UpdateTaskModel(BaseModel):
    name: Optional[str]
    last_completion: Optional[datetime]
    days_between_completions: Optional[float]
    creation_date: Optional[datetime]

    class Config:
        schema_extra = {
            "example": {
                "name": "Vacuum the living room",
                "last_completion": "2032-04-23T10:20:30.400+02:30",
                "days_between_completions": 14.0,
                "creation_date": "2032-04-23T10:20:30.400+02:30"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}