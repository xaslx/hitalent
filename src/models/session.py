from src.models.base import Base
from src.models.user import User
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Session(Base):
    __tablename__ = 'sessions'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    session_uuid: Mapped[str]
    user: Mapped['User'] = relationship('User')