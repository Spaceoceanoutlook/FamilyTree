from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from familytree.models import Photo


class PhotoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, photo_id: int) -> Optional[Photo]:
        stmt = select(Photo).where(Photo.id == photo_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Photo]:
        stmt = select(Photo).order_by(Photo.id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, filename: str, description: Optional[str] = None) -> Photo:
        photo = Photo(filename=filename, description=description)
        self.db.add(photo)
        await self.db.flush()
        return photo

    async def delete(self, photo: Photo) -> None:
        await self.db.delete(photo)
