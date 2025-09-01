from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class AnswerCreateSchema(BaseModel):
    text: str = Field(max_length=500, min_length=10)


class AnswerReadSchema(BaseModel):
    id: int
    text: str
    question_id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)