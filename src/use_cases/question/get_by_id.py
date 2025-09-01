from dataclasses import dataclass

from src.models.question import Question
from src.repositories.base import BaseRepository
from src.schemas.question import QuestionWithAnswersReadSchema


@dataclass
class GetQuestionByIdUseCase:

    question_repository: BaseRepository[Question]

    async def execute(self, question_id: int) -> QuestionWithAnswersReadSchema | None:

        question: Question | None = await self.question_repository.get_by_id(obj_id=question_id)
        
        if not question:
            return None
        
        return QuestionWithAnswersReadSchema.model_validate(question)