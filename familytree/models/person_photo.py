from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from familytree.models import Base


class PersonPhoto(Base):
    __tablename__ = "person_photos"

    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id", ondelete="CASCADE"),
        primary_key=True,
    )

    photo_id: Mapped[int] = mapped_column(
        ForeignKey("photos.id", ondelete="CASCADE"),
        primary_key=True,
    )

    person: Mapped["Person"] = relationship(back_populates="person_photos")
    photo: Mapped["Photo"] = relationship(back_populates="person_photos")
