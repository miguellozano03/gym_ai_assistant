from datetime import time

from pydantic import BaseModel, field_validator

from app.domain.entities.business import WeekDay


class BusinessHoursIntervalSchema(BaseModel):
    id: int | None = None
    description: str | None = None
    opens_at: time
    closes_at: time


class BusinessHoursCreateSchema(BaseModel):
    id: int | None = None
    day: WeekDay
    intervals: list[BusinessHoursIntervalSchema]


class BusinessHoursUpdateSchema(BaseModel):
    id: int | None = None
    day: WeekDay | None = None
    intervals: list[BusinessHoursIntervalSchema] | None = None

    @field_validator("*")
    @classmethod
    def prevent_null(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value
