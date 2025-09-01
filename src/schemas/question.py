from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from src.schemas.answer import AnswerReadSchema


class QuestionCreateSchema(BaseModel):
    text: str = Field(max_length=200, min_length=10)

class QuestionReadSchema(BaseModel):
    id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionWithAnswersReadSchema(QuestionReadSchema):
    answers: list[AnswerReadSchema]