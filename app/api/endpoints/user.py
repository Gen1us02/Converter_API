from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas.user import UserSchema, UserInDB, UserUpdateSchema
from app.repositories.user_repository import UserRepository, get_user_repository
from app.core.security import generate_jwt_token
from app.utils.hash import verify_password
from typing import Dict


auth_router = APIRouter()


@auth_router.post("/login")
async def login(
    user: UserSchema, repo: UserRepository = Depends(get_user_repository)
) -> Dict:
    db_user = await repo.get_user(user.username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = await generate_jwt_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@auth_router.post("/register", response_model=UserInDB)
async def register(
    user: UserSchema, repo: UserRepository = Depends(get_user_repository)
):
    try:
        db_user = await repo.create_user(user)
        return UserInDB(
            id=db_user.id, username=db_user.username, hashed_password=db_user.password
        )
    except ValueError:
        raise HTTPException(status_code=409, detail="User already exists")
