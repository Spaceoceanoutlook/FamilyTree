from familytree.logging_config import search_logger
from familytree.repositories.person import PersonRepository
from familytree.utils.tree_builder import (
    attach_children,
    attach_parent,
    attach_siblings,
    build_node,
)


class TreeService:
    def __init__(self, repo: PersonRepository):
        self.repo = repo
        self.db = repo.db

    async def get_tree(self, person_id: int):
        root = await self.repo.get_by_id(person_id)
        if not root:
            raise ValueError("Person not found")

        logger_str = f"{root.first_name} {root.last_name or ''} {root.birth_year or ''} {root.death_year or ''}".strip()
        search_logger.info(f"Просмотр дерева: {logger_str}")

        visited: set[int] = set()

        return await self._build_recursive(
            root,
            visited,
            include_parents=True,
            include_children=True,
            include_siblings=True,
        )

    async def _build_recursive(
        self,
        person,
        visited: set[int],
        include_parents: bool = True,
        include_children: bool = True,
        include_siblings: bool = False,
    ):
        if not person or person.id in visited:
            return None

        visited.add(person.id)
        node = build_node(person)

        if include_parents:
            for parent_id, key in [
                (person.father_id, "father"),
                (person.mother_id, "mother"),
            ]:
                if parent_id:
                    parent = await self.repo.get_by_id(parent_id)
                    parent_node = await self._build_recursive(
                        parent,
                        visited,
                        include_parents=True,
                        include_children=False,
                        include_siblings=True,
                    )
                    attach_parent(node, key, parent_node)

        if include_siblings:
            siblings = await self.repo.get_siblings(person.id)
            sibling_nodes = []

            for sibling in siblings:
                sib_node = await self._build_recursive(
                    sibling,
                    visited,
                    include_parents=False,
                    include_children=True,
                    include_siblings=False,
                )
                if sib_node:
                    sibling_nodes.append(sib_node)

            attach_siblings(node, sibling_nodes)

        if include_children:
            children = await self.repo.get_children(person.id)
            spouse_id = None
            child_nodes = []

            for child in children:
                if child.father_id and child.father_id != person.id:
                    spouse_id = child.father_id
                elif child.mother_id and child.mother_id != person.id:
                    spouse_id = child.mother_id

                child_node = await self._build_recursive(
                    child,
                    visited,
                    include_parents=False,
                    include_children=True,
                    include_siblings=False,
                )

                if child_node:
                    child_nodes.append(child_node)

            attach_children(node, child_nodes)

            if spouse_id:
                spouse = await self.repo.get_by_id(spouse_id)
                if spouse and spouse.id not in visited:
                    spouse_node = await self._build_recursive(
                        spouse,
                        visited,
                        include_parents=True,
                        include_children=False,
                        include_siblings=True,
                    )
                    if spouse_node:
                        node["spouse"] = spouse_node
        return node
