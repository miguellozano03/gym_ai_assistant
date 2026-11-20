from decimal import Decimal

from pydantic import BaseModel, field_validator


class ProductCreateSchema(BaseModel):
    name: str
    price: Decimal
    available: bool
    description: str | None = None


class ProductUpdateSchema(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    available: bool | None = None
    description: str | None = None

    @field_validator("*")
    @classmethod
    def prevent_null(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value