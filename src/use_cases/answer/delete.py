from dataclasses import dataclass
from fastapi import status, HTTPException
from src.models.answer import Answer
from src.repositories.base import BaseRepository
from src.schemas.user import UserReadSchema


@dataclass
class DeleteAnswerUseCase:

    answer_repository: BaseRepository[Answer]

    async def execute(self, answer_id: int, user: UserReadSchema) -> bool:

        answer: Answer | None = await self.answer_repository.get_by_id(obj_id=answer_id)

        if not answer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого ответа нет.')
        
        if answer.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав.')

        await self.answer_repository.delete(obj=answer)
        return True