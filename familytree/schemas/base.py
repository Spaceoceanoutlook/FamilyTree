from typing import Optional

from pydantic import BaseModel, ConfigDict


class PersonRef(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PhotoRef(BaseModel):
    id: int
    filename: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
