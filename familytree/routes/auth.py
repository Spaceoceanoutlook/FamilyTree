from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from familytree.auth import (
    create_access_token,
    get_current_admin,
    verify_password,
)
from familytree.schemas.auth import Token, TokenData
from settings import settings

router = APIRouter(tags=["Auth"])


@router.post("/auth/token", response_model=Token)
async def login_for_access_token(
    form: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """
    Получение JWT токена для администратора

    - **username**: имя пользователя (для админа: "admin")
    - **password**: пароль администратора
    """
    if form.username != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form.password, settings.hashed_admin_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": "admin"}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.get("/auth/me", summary="Получить информацию о текущем пользователе")
async def read_users_me(current_admin: TokenData = Depends(get_current_admin)) -> dict:
    return {"username": current_admin.username, "role": "admin"}
