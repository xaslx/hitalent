from src.models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.answer import Answer


class Question(Base):
    __tablename__ = 'questions'

    text: Mapped[str] = mapped_column(String(200))

    answers: Mapped[list['Answer']] = relationship(
        'Answer',
        back_populates='question',
        cascade='all, delete-orphan',
        lazy='selectin',
    )
