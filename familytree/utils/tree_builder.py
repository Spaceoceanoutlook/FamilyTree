from typing import Dict, List, Optional, Set

from familytree.models import Person


def build_node(
    person: Person,
) -> Dict:

    node = {
        "id": person.id,
        "first_name": person.first_name,
        "last_name": person.last_name,
    }
    if person.birth_year is not None:
        node["birth_year"] = person.birth_year
    if person.death_year is not None:
        node["death_year"] = person.death_year
    return node


def attach_children(
    node: Dict,
    children: List[Dict],
):
    if children:
        node["children"] = children


def attach_parent(
    node: Dict,
    key: str,
    parent: Dict | None,
):
    if parent:
        node[key] = parent
