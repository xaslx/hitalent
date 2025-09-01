from dataclasses import dataclass
from src.models.user import User
from src.repositories.base import BaseRepository
from src.schemas.user import UserReadSchema, UserCreateSchema
from fastapi import HTTPException, status
from src.utils.hash_password import hash_password


@dataclass
class RegisterUserUseCase:

    user_repository: BaseRepository[User]

    async def execute(self, schema: UserCreateSchema) -> UserReadSchema:
        
        user: User | None = await self.user_repository.get_by_username(username=schema.username)

        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Такой пользователь уже зарегистрирован.')
        
        hashed_password: str = hash_password(password=schema.password)
        new_user: User = User(username=schema.username, hashed_password=hashed_password)

        new_user = await self.user_repository.add(obj=new_user)

        return UserReadSchema.model_validate(new_user)