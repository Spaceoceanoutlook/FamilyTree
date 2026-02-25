from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from familytree.utils.normalization import normalize_russian_text


class GenderEnum(str, Enum):
    M = "M"
    F = "F"


class PersonBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    gender: Optional[GenderEnum] = None
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

    @field_validator("gender", mode="before")
    @classmethod
    def validate_gender(cls, v):
        if v is None:
            return None
        return GenderEnum(v.upper())

    model_config = ConfigDict(from_attributes=True)


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[GenderEnum] = None
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

    @field_validator("gender", mode="before")
    @classmethod
    def validate_gender(cls, v):
        if v is None:
            return None
        return GenderEnum(v.upper())

    model_config = ConfigDict(from_attributes=True)


class PersonOut(PersonBase):
    id: int


class PersonSearch(BaseModel):
    first_name: Optional[str] = Field(default=None, description="Фильтр по имени")
    last_name: Optional[str] = Field(default=None, description="Фильтр по фамилии")

    @field_validator("first_name", "last_name", mode="before")
    @classmethod
    def normalize_names(cls, v: str | None) -> str | None:
        return normalize_russian_text(v)
