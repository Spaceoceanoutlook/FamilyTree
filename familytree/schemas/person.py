from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class PersonBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None

    birth_year: Optional[int] = None
    death_year: Optional[int] = None

    mother_id: Optional[int] = None
    father_id: Optional[int] = None

    @field_validator(
        "father_id", "mother_id", "birth_year", "death_year", mode="before"
    )
    @classmethod
    def zero_to_none(cls, v):
        return None if v == 0 else v

    model_config = ConfigDict(from_attributes=True)


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    mother_id: Optional[int] = None
    father_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class PersonOut(PersonBase):
    id: int
