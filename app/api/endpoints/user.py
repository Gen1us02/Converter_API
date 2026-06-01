from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.api.schemas.user import UserSchema, UserInDB, UserUpdateSchema
from app.repositories.user_repository import UserRepository, get_user_repository
from app.core.security import generate_jwt_token
from app.utils.hash import verify_password
from typing import Dict


auth_router = APIRouter()


@auth_router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(), repo: UserRepository = Depends(get_user_repository)
) -> Dict:
    db_user = await repo.get_user(form.username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(form.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = await generate_jwt_token({"sub": form.username})
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


@auth_router.get("/{username}", response_model=UserInDB)
async def get_user(username: str, repo: UserRepository = Depends(get_user_repository)):
    user = await repo.get_user(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserInDB(id=user.id, username=user.username, hashed_password=user.password)


@auth_router.delete("/delete/{username}")
async def delete_user(
    username: str, repo: UserRepository = Depends(get_user_repository)
) -> Dict:
    try:
        user_id = await repo.delete_user(username)
        if user_id is None:
            raise HTTPException(status_code=404, detail="User not found")

        return {"delete_user_id": user_id}
    except ValueError:
        raise HTTPException(status_code=409, detail="User already exists")


@auth_router.put("/update/{username}")
async def update_user(
    username: str,
    new_user: UserUpdateSchema,
    repo: UserRepository = Depends(get_user_repository),
) -> Dict:
    try:
        user_id = await repo.update_user(username, new_user)
        if user_id is None:
            raise HTTPException(status_code=404, detail="User not found")

        return {"update_user_id": user_id}
    except ValueError:
        raise HTTPException(status_code=409, detail="User already exists")
