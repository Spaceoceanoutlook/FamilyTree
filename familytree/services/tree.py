from familytree.repositories.person import PersonRepository
from familytree.utils.tree_builder import (
    attach_children,
    attach_parent,
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
        visited: set[int] = set()
        return await self._build_recursive(root, visited)

    async def _build_recursive(
        self,
        person,
        visited: set[int],
        include_parents: bool = True,
        include_children: bool = True,
    ):
        if not person or person.id in visited:
            return None
        visited.add(person.id)
        node = build_node(person)
        # parents
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
                    )
                    attach_parent(node, key, parent_node)
        # children
        if include_children:
            children = await self.repo.get_children(person.id)

            spouse_id = None
            child_nodes = []

            for child in children:
                # detect spouse
                if child.father_id and child.father_id != person.id:
                    spouse_id = child.father_id

                elif child.mother_id and child.mother_id != person.id:
                    spouse_id = child.mother_id

                child_node = await self._build_recursive(
                    child,
                    visited,
                    include_parents=False,
                    include_children=True,
                )

                if child_node:
                    child_nodes.append(child_node)

            attach_children(node, child_nodes)

            # attach spouse with parents (no children)
            if spouse_id:
                spouse = await self.repo.get_by_id(spouse_id)

                if spouse and spouse.id not in visited:
                    spouse_node = await self._build_recursive(
                        spouse,
                        visited,
                        include_parents=True,
                        include_children=False,
                    )

                    if spouse_node:
                        node["spouse"] = spouse_node
        return node
