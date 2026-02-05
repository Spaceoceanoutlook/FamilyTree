from typing import Dict, Optional, Set

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from familytree.models import Person


async def build_tree(
    person: Person,
    db: AsyncSession = None,
    visited_ids: Optional[Set[int]] = None,
    include_parents: bool = True,
    include_children: bool = True,
):
    if visited_ids is None:
        visited_ids = set()

    if not person or person.id in visited_ids:
        return None

    visited_ids.add(person.id)

    tree = {
        "id": person.id,
        "first_name": person.first_name,
        "last_name": person.last_name,
    }

    if person.birth_year is not None:
        tree["birth_year"] = person.birth_year

    if person.death_year is not None:
        tree["death_year"] = person.death_year

    if include_parents:
        if person.father_id and db:
            stmt = (
                select(Person)
                .options(selectinload(Person.father))
                .options(selectinload(Person.mother))
                .where(Person.id == person.father_id)
            )
            result = await db.execute(stmt)
            father = result.scalar_one_or_none()
            if father:
                father_data = await build_tree(
                    father,
                    db,
                    visited_ids.copy(),
                    include_parents=True,
                    include_children=False,
                )
                if father_data:
                    tree["father"] = father_data

        if person.mother_id and db:
            stmt = (
                select(Person)
                .options(selectinload(Person.father))
                .options(selectinload(Person.mother))
                .where(Person.id == person.mother_id)
            )
            result = await db.execute(stmt)
            mother = result.scalar_one_or_none()
            if mother:
                mother_data = await build_tree(
                    mother,
                    db,
                    visited_ids.copy(),
                    include_parents=True,
                    include_children=False,
                )
                if mother:
                    tree["mother"] = mother_data

    children = []
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
                    db,
                    visited_ids.copy(),
                    include_parents=False,
                    include_children=True,
                )
                if child:
                    children.append(child_data)

    if children:
        tree["children"] = children

    return tree
