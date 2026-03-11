import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from settings import settings


async def save_upload_file(file: UploadFile) -> str:
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = Path(settings.photo_upload_dir) / unique_filename

    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Не удалось сохранить файл: {str(e)}",
        )

    return unique_filename


async def delete_file(filename: str) -> bool:
    file_path = Path(settings.photo_upload_dir) / filename

    try:
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    except Exception as e:
        print(f"Не удалось удалить файл {filename}: {e}")
        return False


def get_photo_url(filename: str) -> str:
    return f"{settings.photo_url_prefix}/{filename}"
