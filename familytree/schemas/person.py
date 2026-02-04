from pydantic import BaseModel, ConfigDict
from typing import Optional


class PersonBase(BaseModel):
    first_name: str
    last_name: str

    birth_date: Optional[int] = None
    death_date: Optional[int] = None

    father_id: Optional[int] = None
    mother_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class PersonCreate(PersonBase):
    pass


class PersonUpdate(PersonBase):
    pass


class PersonOut(PersonBase):
    id: int
