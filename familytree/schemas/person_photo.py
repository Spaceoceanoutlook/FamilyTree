from pydantic import BaseModel


class PersonPhotoCreate(BaseModel):
    person_id: int
    photo_id: int
