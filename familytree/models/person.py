from familytree.models import Base
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    death_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    birth_year: Mapped[int | None] = mapped_column(Integer, nullable=True)

    father_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("persons.id"), nullable=True
    )
    mother_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("persons.id"), nullable=True
    )

    father: Mapped["Person"] = relationship(
        "Person",
        foreign_keys=[father_id],
        remote_side=[id],
        backref="children_from_father",
    )

    mother: Mapped["Person"] = relationship(
        "Person",
        foreign_keys=[mother_id],
        remote_side=[id],
        backref="children_from_mother",
    )
