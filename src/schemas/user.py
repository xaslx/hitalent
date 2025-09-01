from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserCreateSchema(BaseModel):
    username: str
    password: str

class UserLoginSchema(UserCreateSchema):
    ...

class UserReadSchema(BaseModel):
    id: int
    created_at: datetime
    username: str

    model_config = ConfigDict(from_attributes=True)