import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from settings import settings

ADMIN_PASSWORD = settings.admin_password
security = HTTPBasic()


def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)

    if not correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials
