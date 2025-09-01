from dataclasses import dataclass
from src.repositories.base import BaseRepository
from src.models.question import Question
from src.schemas.question import QuestionCreateSchema, QuestionReadSchema


@dataclass
class CreateQuestionUseCase:
    question_repository: BaseRepository[Question]

    async def execute(self, schema: QuestionCreateSchema) -> QuestionReadSchema:

        question: Question = Question(text=schema.text)
        question = await self.question_repository.add(obj=question)

        return QuestionReadSchema.model_validate(question)