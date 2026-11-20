from decimal import Decimal

from pydantic import BaseModel, field_validator


class MembershipPlanCreateSchema(BaseModel):
    name: str
    price: Decimal
    duration_days: int
    description: str | None = None


class MembershipPlanUpdateSchema(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    duration_days: int | None = None
    description: str | None = None

    @field_validator("*")
    @classmethod
    def prevent_null(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value