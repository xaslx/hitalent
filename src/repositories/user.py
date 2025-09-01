from dataclasses import dataclass
from src.repositories.base import BaseRepository
from src.models.user import User
from sqlalchemy import select
from typing import Type


@dataclass
class SQLAlchemyUserRepository(BaseRepository[User]):

    model: Type[User] = User

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(self.model).where(self.model.username == username)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()