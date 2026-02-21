from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from familytree.auth import get_current_admin
from familytree.database import get_db
from familytree.repositories.feedback import FeedbackRepository
from familytree.schemas.feedback import FeedbackCreate, FeedbackOut
from familytree.services.feedback import FeedbackService

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)


def get_feedback_service(
    db: AsyncSession = Depends(get_db),
) -> FeedbackService:
    repo = FeedbackRepository(db)
    return FeedbackService(repo)


@router.get(
    "/",
    response_model=list[FeedbackOut],
    dependencies=[Depends(get_current_admin)],
)
async def get_feedbacks(
    service: FeedbackService = Depends(get_feedback_service),
):
    return await service.get_all()


@router.post(
    "/",
    response_model=FeedbackOut,
)
async def create_feedback(
    data: FeedbackCreate,
    service: FeedbackService = Depends(get_feedback_service),
):
    return await service.create(data)
