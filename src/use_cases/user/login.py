from dataclasses import dataclass
from src.schemas.user import UserLoginSchema
from src.models.user import User
from src.repositories.base import BaseRepository
from fastapi import status, HTTPException
from src.utils.hash_password import verify_password
from uuid import uuid4
from src.models.session import Session



@dataclass
class LoginUserUseCase:

    user_repository: BaseRepository[User]
    session_repository: BaseRepository[Session]

    async def execute(self, schema: UserLoginSchema) -> str:

        user: User | None = await self.user_repository.get_by_username(username=schema.username)


        if not user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Неверный логин или пароль.')
        
        if verify_password(password=schema.password, hashed=user.hashed_password):
            session_uuid: str = str(uuid4())
            session: Session = Session(user_id=user.id, session_uuid=session_uuid)
            await self.session_repository.add(obj=session)
            return session_uuid
