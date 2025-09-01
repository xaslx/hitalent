from dataclasses import dataclass
from src.schemas.question import QuestionReadSchema
from src.repositories.base import BaseRepository
from src.models.question import Question


@dataclass
class GetAllQuestionsUseCase:

    question_repository: BaseRepository[Question]

    async def execute(self) -> list[QuestionReadSchema]:

        questions: list[Question] = await self.question_repository.get_all()
        return [QuestionReadSchema.model_validate(q) for q in questions]
