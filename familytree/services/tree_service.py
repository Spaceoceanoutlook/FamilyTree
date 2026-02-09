from typing import Dict, Optional, Set

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from familytree.models import Person


async def build_tree(
    person: Person,
    db: AsyncSession,
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

    # Родители
    if include_parents and db:
        for parent_id, key in [
            (person.father_id, "father"),
            (person.mother_id, "mother"),
        ]:
            if parent_id:
                stmt = select(Person).where(Person.id == parent_id)
                result = await db.execute(stmt)
                parent_person = result.scalar_one_or_none()
                if parent_person:
                    parent_data = await build_tree(
                        parent_person,
                        db,
                        visited_ids,
                        include_parents=True,
                        include_children=False,
                    )
                    if parent_data:
                        tree[key] = parent_data

    # Дети
    if include_children and db:
        stmt = select(Person).where(
            (Person.father_id == person.id) | (Person.mother_id == person.id)
        )
        result = await db.execute(stmt)
        kids = result.scalars().all()
        children = []
        for child in kids:
            if child.id not in visited_ids:
                child_data = await build_tree(
                    child, db, visited_ids, include_parents=False, include_children=True
                )
                if child_data:
                    children.append(child_data)
        if children:
            tree["children"] = children

    return tree
