from typing import Optional

from sqlalchemy.exc import SQLAlchemyError

from familytree.models import Person
from familytree.repositories.person import PersonRepository
from familytree.schemas.person import (
    PersonCreate,
    PersonOut,
    PersonUpdate,
)


class PersonService:
    def __init__(self, repo: PersonRepository):
        self.repo = repo
        self.db = repo.db

    async def get_person_by_id(self, person_id: int) -> PersonOut:
        person = await self.repo.get_by_id(person_id)
        if not person:
            raise ValueError("Person not found")
        return PersonOut.model_validate(person)

    async def get_persons_by_name(
        self, first_name: Optional[str] = None, last_name: Optional[str] = None
    ) -> list[PersonOut]:
        persons = await self.repo.get_by_name(
            first_name=first_name, last_name=last_name
        )
        return [PersonOut.model_validate(p) for p in persons]

    async def get_all(self) -> list[PersonOut]:
        persons = await self.repo.get_all()
        return [PersonOut.model_validate(p) for p in persons]

    async def create(self, data: PersonCreate) -> PersonOut:
        try:
            person = Person(**data.model_dump())
            await self.repo.create(person)
            await self.db.commit()
            await self.db.refresh(person)
            return PersonOut.model_validate(person)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError("DB error") from e

    async def update(
        self,
        person_id: int,
        data: PersonUpdate,
    ) -> PersonOut:

        try:
            person = await self.repo.get_by_id(person_id)
            if not person:
                raise ValueError("Person not found")
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(person, key, value)
            await self.db.commit()
            await self.db.refresh(person)
            return PersonOut.model_validate(person)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError("DB error") from e

    async def delete(self, person_id: int) -> None:
        try:
            person = await self.repo.get_by_id(person_id)
            if not person:
                raise ValueError("Person not found")
            await self.repo.delete(person)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError("DB error") from e
