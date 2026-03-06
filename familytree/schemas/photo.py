from typing import Optional

from pydantic import BaseModel, ConfigDict


class PhotoBase(BaseModel):
    filename: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PhotoCreate(PhotoBase):
    pass


class PhotoOut(PhotoBase):
    id: int


class PhotoUpload(BaseModel):
    description: Optional[str] = None
