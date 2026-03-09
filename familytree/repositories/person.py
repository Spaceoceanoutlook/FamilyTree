from typing import Optional

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from familytree.models import Person, PersonPhoto, Photo


class PersonRepository:
    _PHOTO_LOAD_OPTIONS = selectinload(Person.person_photos).selectinload(
        PersonPhoto.photo
    )

    def __init__(self, db: AsyncSession):
        self.db = db

    def _enrich_with_photos(self, person: Person | None) -> None:
        if person and hasattr(person, "person_photos"):
            person.photos = [link.photo for link in person.person_photos]

    def _enrich_persons_with_photos(self, persons: list[Person]) -> None:
        for person in persons:
            self._enrich_with_photos(person)

    async def get_by_id(self, person_id: int) -> Person | None:
        stmt = (
            select(Person)
            .where(Person.id == person_id)
            .options(self._PHOTO_LOAD_OPTIONS)
        )
        result = await self.db.execute(stmt)
        person = result.scalar_one_or_none()
        self._enrich_with_photos(person)
        return person

    async def get_by_name(
        self, first_name: Optional[str] = None, last_name: Optional[str] = None
    ) -> list[Person]:
        stmt = select(Person).options(self._PHOTO_LOAD_OPTIONS)
        if first_name:
            stmt = stmt.where(func.lower(Person.first_name) == func.lower(first_name))
        if last_name:
            stmt = stmt.where(func.lower(Person.last_name) == func.lower(last_name))
        stmt = stmt.order_by(
            func.lower(Person.last_name), func.lower(Person.first_name)
        )
        result = await self.db.execute(stmt)
        persons = result.scalars().all()
        self._enrich_persons_with_photos(persons)
        return persons

    async def get_all(self) -> list[Person]:
        stmt = select(Person).order_by(Person.id).options(self._PHOTO_LOAD_OPTIONS)
        result = await self.db.execute(stmt)
        persons = result.scalars().all()
        self._enrich_persons_with_photos(persons)
        return persons

    async def create(self, person: Person) -> Person:
        self.db.add(person)
        await self.db.flush()
        person.photos = []
        return person

    async def delete(self, person: Person) -> None:
        await self.db.delete(person)

    async def get_children(self, parent_id: int) -> list[Person]:
        stmt = (
            select(Person)
            .where(
                or_(
                    Person.father_id == parent_id,
                    Person.mother_id == parent_id,
                )
            )
            .order_by(Person.birth_year.asc())
            .options(self._PHOTO_LOAD_OPTIONS)
        )
        result = await self.db.execute(stmt)
        persons = result.scalars().all()
        self._enrich_persons_with_photos(persons)
        return persons

    async def get_siblings(self, person_id: int) -> list[Person]:
        person = await self.get_by_id(person_id)
        if not person:
            return []

        conditions = []
        if person.father_id:
            conditions.append(Person.father_id == person.father_id)
        if person.mother_id:
            conditions.append(Person.mother_id == person.mother_id)

        if not conditions:
            return []

        stmt = (
            select(Person)
            .where(
                and_(
                    or_(*conditions),
                    Person.id != person_id,
                )
            )
            .order_by(Person.birth_year.asc())
            .options(self._PHOTO_LOAD_OPTIONS)
        )
        result = await self.db.execute(stmt)
        persons = result.scalars().all()
        self._enrich_persons_with_photos(persons)
        return persons
