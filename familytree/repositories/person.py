from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from familytree.models import Person


class PersonRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, person_id: int) -> Person | None:
        stmt = select(Person).where(Person.id == person_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(
        self, first_name: Optional[str] = None, last_name: Optional[str] = None
    ) -> list[Person]:
        stmt = select(Person)
        if first_name:
            stmt = stmt.where(func.lower(Person.first_name) == func.lower(first_name))
        if last_name:
            stmt = stmt.where(func.lower(Person.last_name) == func.lower(last_name))
        stmt = stmt.order_by(
            func.lower(Person.last_name), func.lower(Person.first_name)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_all(self) -> list[Person]:
        stmt = select(Person).order_by(Person.id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, person: Person) -> Person:
        self.db.add(person)
        await self.db.flush()
        return person

    async def delete(self, person: Person) -> None:
        await self.db.delete(person)

    async def get_children(self, parent_id: int) -> list[Person]:
        stmt = select(Person).where(
            or_(
                Person.father_id == parent_id,
                Person.mother_id == parent_id,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
