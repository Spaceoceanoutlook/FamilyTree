from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["Frontend"])


@router.get("/", response_class=FileResponse, summary="Главная страница")
async def get_index():
    response = FileResponse("familytree/templates/index.html")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@router.get("/about", response_class=FileResponse, summary="О проекте")
async def get_about():
    return FileResponse("familytree/templates/about.html")
