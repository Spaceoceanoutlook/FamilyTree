from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from familytree.models import Feedback


class FeedbackRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Feedback]:
        stmt = select(Feedback).order_by(Feedback.id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, feedback: Feedback) -> Feedback:
        self.db.add(feedback)
        await self.db.flush()
        return feedback
