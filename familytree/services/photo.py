from sqlalchemy.ext.asyncio import AsyncSession

from familytree.models import Photo
from familytree.repositories.person_photo import PersonPhotoRepository
from familytree.repositories.photo import PhotoRepository


class PhotoService:
    def __init__(self, db: AsyncSession):
        self.photo_repo = PhotoRepository(db)
        self.person_photo_repo = PersonPhotoRepository(db)

    async def create_photo(
        self, filename: str, description: str | None = None
    ) -> Photo:
        photo = Photo(filename=filename, description=description)
        return await self.photo_repo.create(photo)

    async def link_person_to_photo(self, person_id: int, photo_id: int):
        photo = await self.photo_repo.get_by_id(photo_id)
        if not photo:
            raise ValueError(f"Photo id={photo_id} не найден")
        await self.person_photo_repo.link_person_to_photo(person_id, photo_id)

    async def create_and_link_photo(
        self, person_id: int, filename: str, description: str | None = None
    ):
        photo = await self.create_photo(filename, description)
        await self.link_person_to_photo(person_id, photo.id)
        return photo

    async def get_person_photos(self, person_id: int) -> list[Photo]:
        return await self.person_photo_repo.get_person_photos(person_id)

    async def unlink_person_from_photo(self, person_id: int, photo_id: int):
        await self.person_photo_repo.unlink_person_from_photo(person_id, photo_id)
