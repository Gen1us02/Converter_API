from pydantic import BaseModel, field_validator
from typing import Any


class UserSchema(BaseModel):
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def ensure_length(cls, v: Any):
        if len(v) < 8:
            raise ValueError("Password length must be bigger then 8 symbols")

        return v


class UserUpdateSchema(BaseModel):
    username: str | None = None
    password: str | None = None


class UserInDB(BaseModel):
    id: int
    username: str
    hashed_password: str
