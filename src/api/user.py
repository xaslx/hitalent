from fastapi import APIRouter, Response, status
from dishka.integrations.fastapi import inject, FromDishka as Depends

from src.schemas.user import UserCreateSchema, UserReadSchema, UserLoginSchema
from src.use_cases.user.create import RegisterUserUseCase
from src.use_cases.user.login import LoginUserUseCase


router: APIRouter = APIRouter()


@router.post(
    '/register',
    description='Эндпоинт для регистрации пользователя',
    status_code=status.HTTP_201_CREATED,
)
@inject
async def register_user(
    new_user: UserCreateSchema,
    use_case: Depends[RegisterUserUseCase],
) -> UserReadSchema:
    
    res: UserReadSchema = await use_case.execute(schema=new_user)
    return res


@router.post(
    '/login',
    description='Эндпоинт для входа пользователя',
    status_code=status.HTTP_200_OK,
)
@inject
async def login_user(
    response: Response,
    login_schema: UserLoginSchema,
    use_case: Depends[LoginUserUseCase]
) -> None:
    
    session_uuid: str = await use_case.execute(schema=login_schema)
    response.set_cookie(key='session', value=session_uuid, httponly=True)





@router.post(
    '/logout',
    description='Эндпоинт для выхода пользователя',
    status_code=status.HTTP_200_OK,
)
@inject
async def logout_user(response: Response) -> None:
    response.delete_cookie(key='session')