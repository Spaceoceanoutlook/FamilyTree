from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from familytree.auth import get_current_admin
from familytree.database import get_db
from familytree.logging_config import search_logger
from familytree.repositories.person import PersonRepository
from familytree.schemas.person import (
    PersonCreate,
    PersonOut,
    PersonSearch,
    PersonUpdate,
)
from familytree.services.person import PersonService
from familytree.utils.client_info import get_client_info

router = APIRouter(
    prefix="/person",
    tags=["Person"],
)


def get_person_service(
    db: AsyncSession = Depends(get_db),
) -> PersonService:
    repo = PersonRepository(db)
    return PersonService(repo)


@router.get("/", response_model=list[PersonOut])
async def get_persons(
    request: Request,
    search_params: PersonSearch = Depends(),
    service: PersonService = Depends(get_person_service),
):
    ip, user_agent = get_client_info(request)

    logger_str = (
        f"{search_params.first_name or ''} {search_params.last_name or ''}".strip()
    )
    search_logger.info(logger_str, extra={"ip": ip, "user_agent": user_agent})

    if search_params.first_name or search_params.last_name:
        return await service.get_persons_by_name(
            first_name=search_params.first_name, last_name=search_params.last_name
        )
    return await service.get_all()


@router.post(
    "/",
    response_model=PersonOut,
    dependencies=[Depends(get_current_admin)],
)
async def create_person(
    data: PersonCreate,
    service: PersonService = Depends(get_person_service),
):
    return await service.create(data)


@router.get(
    "/{person_id}",
    response_model=PersonOut,
)
async def get_person_by_id(
    person_id: int,
    service: PersonService = Depends(get_person_service),
):
    try:
        return await service.get_person_by_id(person_id)
    except ValueError:
        raise HTTPException(404, "Person not found")


@router.patch(
    "/{person_id}",
    response_model=PersonOut,
    dependencies=[Depends(get_current_admin)],
)
async def update_person(
    person_id: int,
    data: PersonUpdate,
    service: PersonService = Depends(get_person_service),
):
    try:
        return await service.update(person_id, data)
    except ValueError:
        raise HTTPException(404, "Person not found")


@router.delete(
    "/{person_id}",
    dependencies=[Depends(get_current_admin)],
)
async def delete_person(
    person_id: int,
    service: PersonService = Depends(get_person_service),
):
    try:
        await service.delete(person_id)
        return {"status": "deleted", "id": person_id}
    except ValueError:
        raise HTTPException(404, "Person not found")
