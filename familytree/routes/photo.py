from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Path,
    UploadFile,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from familytree.auth import get_current_admin
from familytree.database import get_db
from familytree.schemas.photo import PhotoOut
from familytree.services.photo import PhotoService
from familytree.utils.file import delete_file, save_upload_file

router = APIRouter(prefix="/photos", tags=["Photos"])


def get_photo_service(db: AsyncSession = Depends(get_db)) -> PhotoService:
    return PhotoService(db)


@router.post(
    "/",
    response_model=PhotoOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
)
async def upload_photo(
    file: UploadFile = File(...),
    description: str | None = Form(None),
    service: PhotoService = Depends(get_photo_service),
    db: AsyncSession = Depends(get_db),
):
    filename = await save_upload_file(file)

    try:
        photo = await service.create_photo(filename, description)
        await db.commit()
        return photo
    except Exception as e:
        await db.rollback()
        await delete_file(filename)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка сохранения: {str(e)}",
        )


@router.get("/", response_model=list[PhotoOut])
async def get_all_photos(
    service: PhotoService = Depends(get_photo_service),
):
    photos = await service.get_all_photos()
    return photos


@router.get("/persons/{person_id}", response_model=list[PhotoOut])
async def get_person_photos(
    person_id: int = Path(...),
    service: PhotoService = Depends(get_photo_service),
):
    photos = await service.get_person_photos(person_id)
    return photos


@router.post("/{photo_id}/persons/{person_id}", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_admin)])
async def link_person(
    photo_id: int = Path(...),
    person_id: int = Path(...),
    service: PhotoService = Depends(get_photo_service),
    db: AsyncSession = Depends(get_db),
):
    try:
        await service.link_person_to_photo(person_id, photo_id)
        await db.commit()
        return {"status": "linked", "photo_id": photo_id, "person_id": person_id}
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка сохранения: {str(e)}",
        )


@router.delete(
    "/{photo_id}/persons/{person_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_admin)]
)
async def unlink_person(
    photo_id: int = Path(...),
    person_id: int = Path(...),
    service: PhotoService = Depends(get_photo_service),
    db: AsyncSession = Depends(get_db),
):
    await service.unlink_person_from_photo(person_id, photo_id)
    await db.commit()
    return None


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_admin)])
async def delete_photo(
    photo_id: int = Path(...),
    service: PhotoService = Depends(get_photo_service),
    db: AsyncSession = Depends(get_db),
):
    try:
        filename = await service.delete_photo(photo_id)
        await db.commit()

        try:
            await delete_file(filename)
        except Exception as file_err:
            print(
                f"Warning: DB deleted, but file {filename} removal failed: {file_err}"
            )

    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка сохранения: {str(e)}",
        )
