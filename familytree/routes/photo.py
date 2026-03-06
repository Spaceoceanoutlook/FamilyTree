from typing import List
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import os

from familytree.database import get_db
from familytree.schemas.photo import PhotoOut
from familytree.services.photo_service import PhotoService

router = APIRouter(prefix="/photos", tags=["Photos"])

PHOTO_DIR = "static/photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

@router.post("/upload/", response_model=PhotoOut)
async def upload_and_attach_photo(
    person_id: int = Form(...),
    file: UploadFile = File(...),
    description: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
):
    # Сохраняем файл на диск
    filename_on_disk = os.path.join(PHOTO_DIR, file.filename)
    try:
        with open(filename_on_disk, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось сохранить файл: {e}")

    service = PhotoService(db)

    try:
        photo = await service.upload_and_attach(person_id, file.filename, description)
        await db.commit()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка БД: {e}")

    return photo


@router.get("/person/{person_id}", response_model=List[PhotoOut])
async def get_person_photos(person_id: int, db: AsyncSession = Depends(get_db)):
    service = PhotoService(db)
    return await service.get_photos_for_person(person_id)