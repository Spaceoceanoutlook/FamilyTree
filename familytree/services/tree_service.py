from typing import Dict, Optional, Set

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from familytree.models import Person


async def build_tree(
    person: Person,
    max_depth: int = 3,
    current_depth: int = 0,
    db: AsyncSession = None,
    visited_ids: Optional[Set[int]] = None,
    include_parents: bool = True,
    include_children: bool = True,
):
    if visited_ids is None:
        visited_ids = set()

    if not person or current_depth >= max_depth or person.id in visited_ids:
        return None

    visited_ids.add(person.id)

    tree = {
        "id": person.id,
        "first_name": person.first_name,
        "last_name": person.last_name,
        "birth_year": person.birth_year,
        "death_year": person.death_year,
    }

    tree["father"] = None
    tree["mother"] = None

    # Загружаем родителей, но **не загружаем их детей**
    if include_parents:
        if person.father_id and db:
            stmt = (
                select(Person)
                .options(selectinload(Person.father))  # <- загружаем отца отца
                .options(selectinload(Person.mother))  # <- загружаем мать отца
                # .options(selectinload(Person.children_from_father))  # <- не загружаем детей отца
                # .options(selectinload(Person.children_from_mother))  # <- не загружаем детей матери
                .where(Person.id == person.father_id)
            )
            result = await db.execute(stmt)
            father = result.scalar_one_or_none()
            if father:
                tree["father"] = await build_tree(
                    father,
                    max_depth,
                    current_depth + 1,
                    db,
                    visited_ids.copy(),
                    include_parents=True,
                    include_children=False,  # <- не загружаем детей у родителей
                )

        if person.mother_id and db:
            stmt = (
                select(Person)
                .options(selectinload(Person.father))  # <- отец матери
                .options(selectinload(Person.mother))  # <- мать матери
                # .options(selectinload(Person.children_from_father))
                # .options(selectinload(Person.children_from_mother))
                .where(Person.id == person.mother_id)
            )
            result = await db.execute(stmt)
            mother = result.scalar_one_or_none()
            if mother:
                tree["mother"] = await build_tree(
                    mother,
                    max_depth,
                    current_depth + 1,
                    db,
                    visited_ids.copy(),
                    include_parents=True,
                    include_children=False,  # <- не загружаем детей у родителей
                )

    children = []

    # Загружаем детей **только для текущего человека**
    if include_children and db:
        stmt = (
            select(Person)
            .options(selectinload(Person.father))
            .options(selectinload(Person.mother))
            .options(selectinload(Person.children_from_father))
            .options(selectinload(Person.children_from_mother))
            .where((Person.father_id == person.id) | (Person.mother_id == person.id))
        )
        result = await db.execute(stmt)
        kids = result.scalars().all()
        for child in kids:
            if child.id not in visited_ids:
                child_data = await build_tree(
                    child,
                    max_depth,
                    current_depth + 1,
                    db,
                    visited_ids.copy(),
                    include_parents=False,
                    include_children=True,  # <- дети могут иметь родителей, но не их детей
                )
                if child:
                    children.append(child_data)

    tree["children"] = children

    return tree
