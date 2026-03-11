from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from familytree.models import Base


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String)
    year: Mapped[int | None] = mapped_column(Integer)

    person_photos: Mapped[list["PersonPhoto"]] = relationship(
        back_populates="photo",
        cascade="all, delete-orphan",
    )

    persons: list = []
