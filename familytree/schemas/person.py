from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class PersonBase(BaseModel):
    first_name: str
    last_name: str

    birth_year: Optional[int] = None
    death_year: Optional[int] = None

    mother_id: Optional[int] = None
    father_id: Optional[int] = None

    @field_validator("father_id", "mother_id", mode="before")
    @classmethod
    def zero_to_none(cls, v):
        return None if v == 0 else v

    @field_validator("birth_year", "death_year", mode="before")
    @classmethod
    def zero_to_none_year(cls, v):
        return None if v == 0 else v

    model_config = ConfigDict(from_attributes=True)


class PersonCreate(PersonBase):
    pass


class PersonUpdate(PersonBase):
    pass


class PersonOut(PersonBase):
    id: int
