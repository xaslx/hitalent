from dataclasses import dataclass
from src.models.question import Question
from src.repositories.base import BaseRepository
from fastapi import HTTPException, status


@dataclass
class DeleteQuestionUseCase:

    question_repository: BaseRepository[Question]

    async def execute(self, question_id: int) -> bool:

        question: Question | None = await self.question_repository.get_by_id(obj_id=question_id)

        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого вопроса нет.')
        
        await self.question_repository.delete(obj=question)
        return True