from pydantic import BaseModel, field_validator


class TrainerCreateSchema(BaseModel):
    name: str
    description: str | None = None
    specialties: list[str] | None = None
    available: bool = True


class TrainerUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    specialties: list[str] | None = None
    available: bool | None = None

    @field_validator("*")
    @classmethod
    def prevent_null(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value