from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
    

class UserUpdateSchema(BaseModel):
    username: str | None = None
    password: str | None = None


class UserInDB(BaseModel):
    id: int
    username: str
    hashed_password: str
