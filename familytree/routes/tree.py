from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from familytree.database import get_db
from familytree.models import Person
from familytree.services.tree_service import build_tree

router = APIRouter(prefix="/tree", tags=["Tree"])


@router.get(
    "/{person_id}",
    summary="Получить полное дерево родства для человека",
    response_model_exclude_none=True,
)
async def get_tree(
    person_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Person).where(Person.id == person_id)
    result = await db.execute(stmt)
    person = result.scalar_one_or_none()

    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    return await build_tree(person, db=db)
