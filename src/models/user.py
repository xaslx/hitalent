from src.models.base import Base
from sqlalchemy.orm import Mapped



class User(Base):
    __tablename__ = 'users'

    username: Mapped[str]
    hashed_password: Mapped[str]