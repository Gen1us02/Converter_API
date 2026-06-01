from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.schemas.user import UserSchema, UserInDB, UserUpdateSchema
from app.repositories.user_repository import UserRepository, get_user_repository
from app.core.security import generate_jwt_token
from app.utils.hash import verify_password
from typing import Dict


auth_router = APIRouter(tags=["Users API"])


@auth_router.post(
    "/login",
    summary="Endpoint for login user",
    response_description="User's access token",
)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    repo: UserRepository = Depends(get_user_repository),
) -> Dict:
    db_user = await repo.get_user(form.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username"
        )

    if not verify_password(form.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )

    token = await generate_jwt_token({"sub": form.username})
    return {"access_token": token, "token_type": "bearer"}


@auth_router.post(
    "/register",
    summary="Endpoint for register user",
    response_description="New user",
    response_model=UserInDB,
)
async def register(
    user: UserSchema, repo: UserRepository = Depends(get_user_repository)
):
    try:
        db_user = await repo.create_user(user)
        return UserInDB(
            id=db_user.id, username=db_user.username, hashed_password=db_user.password
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )


@auth_router.get(
    "/{username}",
    summary="Endpoint for get user by username",
    response_description="Found user",
    response_model=UserInDB,
)
async def get_user(
    username: str = Path(..., description="User's username"),
    repo: UserRepository = Depends(get_user_repository),
):
    user = await repo.get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserInDB(id=user.id, username=user.username, hashed_password=user.password)


@auth_router.delete(
    "/delete/{username}",
    summary="Endpoint for delete user",
    response_description="Id of delete user",
)
async def delete_user(
    username: str = Path(..., description="User's username"),
    repo: UserRepository = Depends(get_user_repository),
) -> Dict:
    try:
        user_id = await repo.delete_user(username)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return {"delete_user_id": user_id}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User already exists"
        )


@auth_router.put(
    "/update/{username}",
    summary="Endpoint for update user data",
    response_description="Id of update user",
)
async def update_user(
    new_user: UserUpdateSchema,
    username: str = Path(..., description="User's username"),
    repo: UserRepository = Depends(get_user_repository),
) -> Dict:
    try:
        user_id = await repo.update_user(username, new_user)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return {"update_user_id": user_id}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
