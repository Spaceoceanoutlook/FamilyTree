from typing import Optional

from pydantic import BaseModel, ConfigDict

from familytree.schemas.base import PersonRef


class PhotoBase(BaseModel):
    filename: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PhotoCreate(PhotoBase):
    pass


class PhotoOut(PhotoBase):
    id: int
    persons: list[PersonRef] = []


class PhotoUpload(BaseModel):
    description: Optional[str] = None
