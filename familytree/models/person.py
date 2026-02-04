from familytree.models import Base
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    birth_year: Mapped[int] = mapped_column(Integer)
    death_year: Mapped[int] = mapped_column(Integer)

    father_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("persons.id"), nullable=True
    )
    mother_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("persons.id"), nullable=True
    )
