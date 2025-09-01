from fastapi import APIRouter, status, Path, HTTPException
from dishka.integrations.fastapi import inject, FromDishka as Depends
from typing import Annotated
from src.schemas.user import UserReadSchema
from src.schemas.answer import AnswerCreateSchema, AnswerReadSchema
from src.use_cases.answer.create import CreateAnswerUseCase
from src.use_cases.answer.get_by_id import GetAnswerByIdUseCase
from src.use_cases.answer.delete import DeleteAnswerUseCase


router: APIRouter = APIRouter()


@router.post(
    '/questions/{id}/answers',
    description='Эндпоинт добавить ответ к вопросу',
    status_code=status.HTTP_201_CREATED,
)
@inject
async def add_answer(
    id: Annotated[int, Path()],
    use_case: Depends[CreateAnswerUseCase],
    user: Depends[UserReadSchema],
    answer: AnswerCreateSchema,
) -> AnswerReadSchema:
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Для добавления ответа, нужно войти в аккаунт.')

    return await use_case.execute(question_id=id, schema=answer, user_id=user.id)



@router.get(
    '/answers/{id}',
    description='Эндпоинт для получения конкретного ответа',
    status_code=status.HTTP_200_OK,
)
@inject
async def get_answer(
    id: Annotated[int, Path()],
    use_case: Depends[GetAnswerByIdUseCase],
) -> AnswerReadSchema | None:
    
    return await use_case.execute(answer_id=id)



@router.delete(
    '/answers/{id}',
    description='Эндпоинт для удаления ответа',
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_answer(
    id: Annotated[int, Path()],
    user: Depends[UserReadSchema],
    use_case: Depends[DeleteAnswerUseCase],
) -> None:
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Для удаления ответа, нужно войти в аккаунт.')

    await use_case.execute(answer_id=id, user=user)