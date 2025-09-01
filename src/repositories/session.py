from dataclasses import dataclass
from src.repositories.base import BaseRepository
from src.models.session import Session
from sqlalchemy import select
from typing import Type


@dataclass
class SQLAlchemySessionRepository(BaseRepository[Session]):

    model: Type[Session] = Session


    async def get_by_session_uuid(self, session_uuid: str) -> Session | None:
        stmt = select(self.model).where(self.model.session_uuid == session_uuid)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()