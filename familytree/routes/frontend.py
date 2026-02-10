from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["Frontend"])


@router.get("/", response_class=FileResponse, summary="Главная страница")
async def get_index():
    return FileResponse("familytree/templates/index.html")
