from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from familytree.models import Person


class PersonRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, person_id: int) -> Person | None:
        stmt = select(Person).where(Person.id == person_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Person]:
        stmt = select(Person).order_by(Person.last_name)
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
