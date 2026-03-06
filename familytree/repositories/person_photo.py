from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List

from familytree.models import PersonPhoto, Photo

class PersonPhotoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_person_to_photo(self, person_id: int, photo_id: int) -> None:
        link = PersonPhoto(person_id=person_id, photo_id=photo_id)
        self.db.add(link)
        await self.db.flush()

    async def get_photos_for_person(self, person_id: int) -> List[Photo]:
        stmt = (
            select(PersonPhoto)
            .options(selectinload(PersonPhoto.photo))  # 🔹 сразу подгружаем фото
            .where(PersonPhoto.person_id == person_id)
        )
        result = await self.db.execute(stmt)
        links = result.scalars().all()
        return [link.photo for link in links]

    async def remove_person_from_photo(self, person_id: int, photo_id: int) -> None:
        stmt = select(PersonPhoto).where(
            PersonPhoto.person_id == person_id,
            PersonPhoto.photo_id == photo_id,
        )
        result = await self.db.execute(stmt)
        link = result.scalar_one_or_none()
        if link:
            await self.db.delete(link)