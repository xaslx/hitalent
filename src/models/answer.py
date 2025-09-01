from src.models.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.question import Question


class Answer(Base):
    __tablename__ = 'answers'
    
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    text: Mapped[str] = mapped_column(String(length=500))

    question: Mapped['Question'] = relationship(
        'Question',
        back_populates='answers',
    )