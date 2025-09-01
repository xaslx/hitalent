from dataclasses import dataclass
from src.models.answer import Answer
from src.repositories.base import BaseRepository
from src.schemas.answer import AnswerReadSchema



@dataclass
class GetAnswerByIdUseCase:

    answer_repository: BaseRepository[Answer]

    async def execute(self, answer_id: int) -> AnswerReadSchema | None:

        answer: Answer | None = await self.answer_repository.get_by_id(obj_id=answer_id)

        if not answer:
            return None
        
        return AnswerReadSchema.model_validate(answer)