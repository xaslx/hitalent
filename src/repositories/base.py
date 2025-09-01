from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase
from dataclasses import dataclass


T = TypeVar("T", bound=DeclarativeBase)


@dataclass(kw_only=True)
class BaseRepository(Generic[T]):

    model: Type[T]
    session: AsyncSession

    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
        await self.session.commit()
  

    async def get_by_id(self, obj_id: int) -> T | None:
        result = await self.session.get(self.model, obj_id)
        return result

    async def get_all(self) -> list[T]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()
