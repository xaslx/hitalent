from dataclasses import dataclass
from src.repositories.base import BaseRepository
from src.models.question import Question
from typing import Type


@dataclass
class SQLAlchemyQuestionRepository(BaseRepository[Question]):

    model: Type[Question] = Question
