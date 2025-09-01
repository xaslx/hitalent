from fastapi import APIRouter, Path, status
from dishka.integrations.fastapi import inject, FromDishka as Depends
from typing import Annotated
from src.schemas.question import QuestionCreateSchema, QuestionReadSchema, QuestionWithAnswersReadSchema
from src.use_cases.question.create import CreateQuestionUseCase
from src.use_cases.question.get_by_id import GetQuestionByIdUseCase
from src.use_cases.question.delete import DeleteQuestionUseCase
from src.use_cases.question.get_all import GetAllQuestionsUseCase


router: APIRouter = APIRouter()


@router.get(
    '/',
    description='Список всех вопросов',
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all_questions(use_case: Depends[GetAllQuestionsUseCase]) -> list[QuestionReadSchema]:
    
    return await use_case.execute()


@router.post(
    '/',
    description='Эндпоинт для создания вопроса',
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_question(
    question: QuestionCreateSchema,
    use_case: Depends[CreateQuestionUseCase],
) -> QuestionReadSchema:
    
    res: QuestionReadSchema = await use_case.execute(schema=question)
    return res


@router.get(
    '/{id}',
    description='Эндпоинт для получения вопроса и всех ответов',
    status_code=status.HTTP_200_OK,
)
@inject
async def get_question_by_id(
    id: Annotated[int, Path()],
    use_case: Depends[GetQuestionByIdUseCase],
) -> QuestionWithAnswersReadSchema | None:
    
    question: QuestionWithAnswersReadSchema | None = await use_case.execute(question_id=id)
    return question


@router.delete(
    '/{id}',
    description='Эндпоинт для удаления вопроса с его ответами',
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_question_by_id(
    id: Annotated[int, Path()],
    use_case: Depends[DeleteQuestionUseCase],
) -> None:
    
    await use_case.execute(question_id=id)