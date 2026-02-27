from fastapi import APIRouter, Depends, HTTPException, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession

from familytree.database import get_db
from familytree.repositories.person import PersonRepository
from familytree.services.tree import TreeService
from familytree.utils.client_info import get_client_info

router = APIRouter(prefix="/tree", tags=["Tree"])


def get_tree_service(
    db: AsyncSession = Depends(get_db),
):
    repo = PersonRepository(db)
    return TreeService(repo)


@router.get("/{person_id}")
async def get_tree(
    request: Request,
    person_id: int = Path(..., ge=1),
    service: TreeService = Depends(get_tree_service),
):
    ip, ua = get_client_info(request)
    try:
        return await service.get_tree(person_id, client_ip=ip, user_agent=ua)
    except ValueError:
        raise HTTPException(404, "Person not found")
