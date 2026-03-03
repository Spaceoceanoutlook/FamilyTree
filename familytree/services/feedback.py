from sqlalchemy.exc import SQLAlchemyError

from familytree.models import Feedback
from familytree.repositories.feedback import FeedbackRepository
from familytree.schemas.feedback import FeedbackCreate, FeedbackOut
from familytree.logging_config import feedback_logger

class FeedbackService:
    def __init__(self, repo: FeedbackRepository):
        self.repo = repo
        self.db = repo.db

    async def get_all(self) -> list[FeedbackOut]:
        feedback = await self.repo.get_all()
        return [FeedbackOut.model_validate(f) for f in feedback]

    async def create(self, data: FeedbackCreate) -> FeedbackOut:
        try:
            feedback = Feedback(**data.model_dump())
            logger_str = f"Имя: {feedback.name} Связь: {feedback.email or ''} Сообщение: {feedback.message}".strip()
            feedback_logger.info(logger_str)
            await self.repo.create(feedback)
            await self.db.commit()
            await self.db.refresh(feedback)
            return FeedbackOut.model_validate(feedback)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError("DB error") from e
