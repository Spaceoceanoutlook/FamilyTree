from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from familytree.models import Person, PersonPhoto, Photo


class PhotoRepository:
    _PERSON_LOAD_OPTIONS = selectinload(Photo.person_photos).selectinload(
        PersonPhoto.person
    )

    def __init__(self, db: AsyncSession):
        self.db = db

    def _enrich_with_persons(self, photo: Photo | None) -> None:
        if photo and hasattr(photo, "person_photos"):
            photo.persons = [
                {
                    "id": link.person.id,
                    "first_name": link.person.first_name,
                    "last_name": link.person.last_name,
                }
                for link in photo.person_photos
                if link.person
            ]

    def _enrich_photos_with_persons(self, photos: list[Photo]) -> None:
        for photo in photos:
            self._enrich_with_persons(photo)

    async def get_by_id(self, photo_id: int) -> Photo | None:
        stmt = (
            select(Photo).where(Photo.id == photo_id).options(self._PERSON_LOAD_OPTIONS)
        )
        result = await self.db.execute(stmt)
        photo = result.scalar_one_or_none()
        self._enrich_with_persons(photo)
        return photo

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Photo]:
        stmt = (
            select(Photo)
            .order_by(Photo.id.desc())
            .offset(skip)
            .limit(limit)
            .options(self._PERSON_LOAD_OPTIONS)
        )
        result = await self.db.execute(stmt)
        photos = result.scalars().all()
        self._enrich_photos_with_persons(photos)
        return photos

    async def get_by_person_id(self, person_id: int) -> list[Photo]:
        stmt = (
            select(Photo)
            .join(PersonPhoto, Photo.id == PersonPhoto.photo_id)
            .where(PersonPhoto.person_id == person_id)
            .options(self._PERSON_LOAD_OPTIONS)
        )
        result = await self.db.execute(stmt)
        photos = result.scalars().all()
        self._enrich_photos_with_persons(photos)
        return photos

    async def create(self, photo: Photo) -> Photo:
        self.db.add(photo)
        await self.db.flush()
        photo.persons = []
        return photo

    async def delete(self, photo: Photo) -> None:
        await self.db.delete(photo)
