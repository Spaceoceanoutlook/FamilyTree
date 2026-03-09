from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from familytree.models import PersonPhoto, Photo


class PersonPhotoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def link(self, person_id: int, photo_id: int) -> None:
        link = PersonPhoto(person_id=person_id, photo_id=photo_id)
        self.db.add(link)
        await self.db.flush()

    async def unlink(self, person_id: int, photo_id: int) -> None:
        stmt = delete(PersonPhoto).where(
            (PersonPhoto.person_id == person_id) & (PersonPhoto.photo_id == photo_id)
        )
        await self.db.execute(stmt)

    async def get_photos_by_person(self, person_id: int) -> list[Photo]:
        stmt = (
            select(Photo)
            .join(PersonPhoto, Photo.id == PersonPhoto.photo_id)
            .where(PersonPhoto.person_id == person_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def delete_links_by_photo(self, photo_id: int) -> None:
        stmt = delete(PersonPhoto).where(PersonPhoto.photo_id == photo_id)
        await self.db.execute(stmt)
