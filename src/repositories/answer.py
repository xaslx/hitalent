from dataclasses import dataclass
from src.repositories.base import BaseRepository
from src.models.answer import Answer
from typing import Type


@dataclass
class SQLAlchemyAnswerRepository(BaseRepository[Answer]):

    model: Type[Answer] = Answer