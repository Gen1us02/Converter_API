from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.db.models import User
from api.schemas.user import UserSchema, UserUpdateSchema
from typing import Optional


class BaseUserRepository(ABC):
    @abstractmethod
    async def get_user(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def create_user(self, user: UserSchema) -> User:
        pass

    @abstractmethod
    async def delete_user(self, username: str) -> Optional[int]:
        pass

    @abstractmethod
    async def update_user(self, username: str, new_data: UserSchema) -> Optional[int]:
        pass

# TODO: Добавить хеширование пароля при сохранении пользователя в БД
class UserRepository(BaseUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user(self, username: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()

    async def create_user(self, user: UserSchema) -> User:
        try:
            new_user = User(**user.model_dump())
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)

            return new_user
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError(f"DB error: {e}")

    async def delete_user(self, username: str) -> Optional[int]:
        try:
            user = await self.get_user(username)
            if user is None:
                return None

            user_id = user.id
            self.session.delete(user)
            await self.session.commit()

            return user_id
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError(f"DB error: {e}")

    async def update_user(self, username: str, new_data: UserUpdateSchema) -> Optional[int]:
        try:
            user = await self.get_user(username)
            if user is None:
                return None

            update_fields = new_data.model_dump(exclude_unset=True)
            for field, value in update_fields.items():
                setattr(user, field, value)

            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user.id
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError(f"DB error: {e}")
