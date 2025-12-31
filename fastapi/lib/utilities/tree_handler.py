from lib.utilities import errors


class TreeHandler:
    def __init__(self, tree):
        self._tree = tree

    def get_node(self, node_id: str) -> dict | None:
        parts = [p for p in node_id.split("/") if p]

        current: dict = self._tree

        for part in parts[1:]:
            children: list[dict] = current["children"]
            found = None

            for child in children:
                if child["label"] == part:
                    found = child
                    break

            if not found:
                return None

            current = found

        return current

    def get_parent_node(self, node_id: str) -> dict | None:
        parts = [p for p in node_id.split("/") if p]
        if len(parts) <= 1:
            return None

        parent_id = "/" + "/".join(parts[:-1])
        return self.get_node(parent_id)

    def get_children_ids(self, node_id: str) -> list[str]:
        target = self.get_node(node_id)
        result = []
        if target is None:
            return result

        def collect(node: dict):
            for child in node["children"]:
                result.append(child["id"])
                collect(child)

        collect(target)
        return result

    def insert_node(self, new_node: dict) -> None:
        node_id = new_node["id"]
        parent_node = self.get_parent_node(node_id)
        if parent_node is None:
            raise errors.BadRequestError("TreeHandler.invalid_node_id")

        children: list = parent_node["children"]

        for child in children:
            if child["id"] == new_node["id"]:
                raise errors.ConflictError(f"TreeHandler.conflict_node")

        children.append(new_node)

    def delete_node(self, node_id: str) -> None:
        parent_node = self.get_parent_node(node_id)
        if parent_node is None:
            raise errors.NotFoundError("TreeHandler.not_found")

        children: list = parent_node["children"]
        for i, child in enumerate(children):
            if child["id"] == node_id:
                del children[i]
                return

        raise errors.NotFoundError("TreeHandler.not_found")

    def sort_tree(self, tree: dict | None = None) -> dict:
        if tree is None:
            tree = self._tree

        def sort_key(child: dict):
            is_file = not child["children"]
            return (is_file, child["id"])

        children: list = tree["children"]
        children.sort(key=sort_key)

        for child in children:
            self.sort_tree(child)

        return tree
