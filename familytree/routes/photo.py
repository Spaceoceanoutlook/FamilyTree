# api/routes/photo.py
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from familytree.database import get_db
from familytree.schemas.photo import PhotoOut
from familytree.services.photo import PhotoService
from familytree.utils.file import delete_file, get_photo_url, save_upload_file

router = APIRouter(prefix="/photos", tags=["Photos"])


@router.post("/upload", response_model=PhotoOut, status_code=status.HTTP_201_CREATED)
async def upload_photo(
    file: UploadFile = File(...),
    description: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Загрузить фото (без привязки к человеку).
    """
    # Сохраняем файл на диск
    filename = await save_upload_file(file)

    # Создаем запись в БД
    service = PhotoService(db)

    try:
        photo = await service.create_photo(filename=filename, description=description)
        await db.commit()
    except Exception as e:
        await db.rollback()
        # Если ошибка БД - удаляем файл
        await delete_file(filename)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании записи: {str(e)}",
        )

    return photo


@router.post(
    "/upload-and-link", response_model=PhotoOut, status_code=status.HTTP_201_CREATED
)
async def upload_and_link_photo(
    person_id: int = Form(...),
    file: UploadFile = File(...),
    description: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Загрузить фото и сразу привязать к человеку.
    """
    # Сохраняем файл на диск
    filename = await save_upload_file(file)

    # Создаем запись в БД и привязываем к человеку
    service = PhotoService(db)

    try:
        photo = await service.create_and_link_photo(
            person_id=person_id, filename=filename, description=description
        )
        await db.commit()
    except ValueError as e:
        await db.rollback()
        await delete_file(filename)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        await db.rollback()
        await delete_file(filename)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка БД: {str(e)}",
        )

    return photo


@router.get("/person/{person_id}", response_model=List[PhotoOut])
async def get_person_photos(person_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить все фото человека.
    """
    service = PhotoService(db)

    try:
        photos = await service.get_person_photos(person_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return photos


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_photo(photo_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удалить фото (из БД и с диска).
    """
    service = PhotoService(db)

    try:
        # Получаем фото чтобы знать имя файла
        photo = await service.get_photo_by_id(photo_id)
        if not photo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Фото с id {photo_id} не найдено",
            )

        # Удаляем из БД
        await service.delete_photo(photo_id)
        await db.commit()

        # Удаляем файл с диска
        await delete_file(photo.filename)

    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении: {str(e)}",
        )
