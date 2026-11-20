from pydantic import BaseModel, field_validator


class GymPolicyCreateSchema(BaseModel):
    id: int | None = None
    title: str
    description: str
    active: bool = True


class GymPolicyUpdateSchema(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    active: bool | None = None

    @field_validator("*")
    @classmethod
    def prevent_null(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value