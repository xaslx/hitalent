from collections.abc import AsyncIterable

from dishka import Provider, Scope, from_context, provide
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.models.answer import Answer
from src.repositories.answer import SQLAlchemyAnswerRepository
from src.models.session import Session
from src.repositories.session import SQLAlchemySessionRepository
from src.models.user import User
from src.database.postgres import new_session_maker
from src.config import Config
from src.models.question import Question
from src.models.user import User
from src.repositories.base import BaseRepository
from src.repositories.user import SQLAlchemyUserRepository
from src.repositories.question import SQLAlchemyQuestionRepository
from src.use_cases.question.create import CreateQuestionUseCase
from src.use_cases.question.get_by_id import GetQuestionByIdUseCase
from src.use_cases.question.delete import DeleteQuestionUseCase
from src.use_cases.question.get_all import GetAllQuestionsUseCase
from src.use_cases.user.create import RegisterUserUseCase
from src.use_cases.user.login import LoginUserUseCase
from src.schemas.user import UserReadSchema
from src.use_cases.answer.create import CreateAnswerUseCase
from src.use_cases.answer.get_by_id import GetAnswerByIdUseCase
from src.use_cases.answer.delete import DeleteAnswerUseCase


class AppProvider(Provider):

    config = from_context(provides=Config, scope=Scope.APP)
    request: Request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    
    #repository
    @provide(scope=Scope.REQUEST)
    def get_question_repository(self, session: AsyncSession) -> BaseRepository[Question]:
        return SQLAlchemyQuestionRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> BaseRepository[User]:
        return SQLAlchemyUserRepository(session=session)
    
    @provide(scope=Scope.REQUEST)
    def get_session_repository(self, session: AsyncSession) -> BaseRepository[Session]:
        return SQLAlchemySessionRepository(session=session)
    
    @provide(scope=Scope.REQUEST)
    def get_answer_repository(self, session: AsyncSession) -> BaseRepository[Answer]:
        return SQLAlchemyAnswerRepository(session=session)


    #use case Question
    @provide(scope=Scope.REQUEST)
    def get_create_question_use_case(self, question_repository: BaseRepository[Question]) -> CreateQuestionUseCase:
        return CreateQuestionUseCase(question_repository=question_repository)
    
    @provide(scope=Scope.REQUEST)
    def get_question_by_id_use_case(self, question_repository: BaseRepository[Question]) -> GetQuestionByIdUseCase:
        return GetQuestionByIdUseCase(question_repository=question_repository)
    
    @provide(scope=Scope.REQUEST)
    def get_delete_question_use_case(self, question_repository: BaseRepository[Question]) -> DeleteQuestionUseCase:
        return DeleteQuestionUseCase(question_repository=question_repository)
    

    @provide(scope=Scope.REQUEST)
    def get_all_questions_use_case(self, question_repository: BaseRepository[Question]) -> GetAllQuestionsUseCase:
        return GetAllQuestionsUseCase(question_repository=question_repository)
    

    #use case User
    @provide(scope=Scope.REQUEST)
    def get_register_user_use_case(self, user_repository: BaseRepository[User]) -> RegisterUserUseCase:
        return RegisterUserUseCase(user_repository=user_repository)
    
    @provide(scope=Scope.REQUEST)
    def get_login_user_use_case(
        self,
        user_repository: BaseRepository[User],
        session_repository: BaseRepository[Session],
    ) -> LoginUserUseCase:
        return LoginUserUseCase(user_repository=user_repository, session_repository=session_repository)
    

    #use case Answer
    @provide(scope=Scope.REQUEST)
    def get_create_answer_use_case(
        self,
        question_repository: BaseRepository[Question],
        answer_repository: BaseRepository[Answer],
    ) -> CreateAnswerUseCase:
        
        return CreateAnswerUseCase(answer_repository=answer_repository, question_repository=question_repository)


    @provide(scope=Scope.REQUEST)
    def get_answer_by_id_use_case(self, answer_repository: BaseRepository[Answer]) -> GetAnswerByIdUseCase:
        return GetAnswerByIdUseCase(answer_repository=answer_repository)
    

    @provide(scope=Scope.REQUEST)
    def get_delete_answer_use_case(self, answer_repository: BaseRepository[Answer]) -> DeleteAnswerUseCase:
        return DeleteAnswerUseCase(answer_repository=answer_repository)


    #current user
    @provide(scope=Scope.REQUEST)
    async def get_current_user(
        self,
        request: Request,
        session_repository: BaseRepository[Session],
        user_repository: BaseRepository[User],
    ) -> UserReadSchema:

        session_uuid: str | None = request.cookies.get('session')

        if not session_uuid:
            return None
        
        session: Session | None = await session_repository.get_by_session_uuid(session_uuid=session_uuid)
        user: User | None = await user_repository.get_by_id(obj_id=session.user_id)

        if not user:
            return None
        
        return UserReadSchema.model_validate(user)



