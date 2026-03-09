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

    async def get_photo_by_id(self, photo_id: int) -> Photo:
        photo = await self.photo_repo.get_by_id(photo_id)
        if not photo:
            raise ValueError(f"Photo with id {photo_id} not found")
        return photo

    async def get_all_photos(self) -> list[Photo]:
        return await self.photo_repo.get_all()

    async def link_person_to_photo(self, person_id: int, photo_id: int) -> None:
        photo = await self.photo_repo.get_by_id(photo_id)
        if not photo:
            raise ValueError(f"Фото с id={photo_id} не найдено")
        await self.person_photo_repo.link(person_id, photo_id)

    async def get_person_photos(self, person_id: int) -> list[Photo]:
        return await self.photo_repo.get_by_person_id(person_id)

    async def unlink_person_from_photo(self, person_id: int, photo_id: int) -> None:
        await self.person_photo_repo.unlink(person_id, photo_id)

    async def delete_photo(self, photo_id: int) -> str:
        photo = await self.photo_repo.get_by_id(photo_id)
        if not photo:
            raise ValueError(f"Фото с id={photo_id} не найдено")

        filename = photo.filename

        await self.person_photo_repo.delete_links_by_photo(photo_id)
        await self.photo_repo.delete(photo)

        return filename
