from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from familytree.models import Photo
from familytree.repositories.photo import PhotoRepository
from familytree.repositories.person_photo import PersonPhotoRepository

class PhotoService:
    def __init__(self, db: AsyncSession):
        self.photo_repo = PhotoRepository(db)
        self.person_photo_repo = PersonPhotoRepository(db)

    async def create_photo(self, filename: str, description: str | None = None) -> Photo:
        photo = Photo(filename=filename, description=description)
        return await self.photo_repo.create(photo)

    async def attach_person_to_photo(self, person_id: int, photo_id: int):
        photo = await self.photo_repo.get_by_id(photo_id)
        if not photo:
            raise ValueError(f"Photo id={photo_id} не найден")
        await self.person_photo_repo.add_person_to_photo(person_id, photo_id)

    async def upload_and_attach(self, person_id: int, filename: str, description: str | None = None):
        photo = await self.create_photo(filename, description)
        await self.attach_person_to_photo(person_id, photo.id)
        return photo

    async def get_photos_for_person(self, person_id: int) -> List[Photo]:
        return await self.person_photo_repo.get_photos_for_person(person_id)

    async def remove_person_from_photo(self, person_id: int, photo_id: int):
        await self.person_photo_repo.remove_person_from_photo(person_id, photo_id)