from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api.question import router as question_router
from dishka import AsyncContainer, make_async_container
from dishka.integrations import fastapi as fastapi_integration
from src.ioc import AppProvider
from src.config import Config
from src.api.user import router as user_router
from src.api.answer import router as answer_router

@asynccontextmanager
async def lifespa(app: FastAPI):

    yield


def create_app() -> FastAPI:

    config: Config = Config()
    container: AsyncContainer = make_async_container(
        AppProvider(), context={Config: config}
    )

    app: FastAPI = FastAPI(
        title='Hitalent',
    )
    app.include_router(question_router, prefix='/questions', tags=['Вопросы'])
    app.include_router(user_router, tags=['Пользователи'])
    app.include_router(answer_router, tags=['Ответы'])

    fastapi_integration.setup_dishka(container=container, app=app)

    return app