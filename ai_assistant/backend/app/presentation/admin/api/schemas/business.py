from pydantic import BaseModel, field_validator


class BusinessCreateSchema(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None


class BusinessUpdateSchema(BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None

    @field_validator("name", "description")
    @classmethod
    def prevent_null(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value