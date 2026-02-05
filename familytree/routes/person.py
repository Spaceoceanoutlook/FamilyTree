from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from familytree.database import get_db
from familytree.models import Person
from familytree.schemas.person import PersonCreate, PersonOut, PersonUpdate

router = APIRouter(prefix="/person", tags=["Person"])


@router.post("/", summary="Создать нового человека", response_model=PersonOut)
async def create_person(data: PersonCreate, db: AsyncSession = Depends(get_db)):
    new_person = Person(**data.model_dump())
    db.add(new_person)
    await db.commit()
    await db.refresh(new_person)
    return new_person


@router.get(
    "/",
    summary="Получить информацию о всех людях в базе данных",
    response_model=list[PersonOut],
    response_model_exclude_none=True,
)
async def get_persons(db: AsyncSession = Depends(get_db)):
    stmt = select(Person)
    persons = await db.scalars(stmt)
    return persons


@router.get(
    "/{person_id}",
    summary="Получить информацию о человеке",
    response_model=PersonOut,
    response_model_exclude_none=True,
)
async def get_person(person_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Person).where(Person.id == person_id)
    person = await db.scalar(stmt)

    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    return person


@router.patch(
    "/{person_id}",
    summary="Обновить данные человека",
    response_model=PersonOut,
)
async def update_person(
    person_id: int, data: PersonUpdate, db: AsyncSession = Depends(get_db)
):
    stmt = select(Person).where(Person.id == person_id)
    person = await db.scalar(stmt)

    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(person, key, value)

    await db.commit()
    await db.refresh(person)
    return person


@router.delete("/{person_id}", summary="Удалить человека")
async def delete_person(person_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Person).where(Person.id == person_id)
    person = await db.scalar(stmt)

    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    await db.delete(person)
    await db.commit()
    return {"status": "deleted", "id": person_id}
