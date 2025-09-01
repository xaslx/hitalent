from dataclasses import dataclass
from fastapi import status, HTTPException
from src.models.question import Question
from src.schemas.answer import AnswerCreateSchema, AnswerReadSchema
from src.models.answer import Answer
from src.repositories.base import BaseRepository


@dataclass
class CreateAnswerUseCase:

    answer_repository: BaseRepository[Answer]
    question_repository: BaseRepository[Question]

    async def execute(self, question_id: int, schema: AnswerCreateSchema, user_id: int) -> AnswerReadSchema:
        
        question: Question | None = await self.question_repository.get_by_id(obj_id=question_id)

        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Нельзя добавить ответ к несуществующему вопросу.',
            )
        
        answer: Answer = Answer(text=schema.text, user_id=user_id, question_id=question_id)
        answer = await self.answer_repository.add(obj=answer)
        return AnswerReadSchema.model_validate(answer)