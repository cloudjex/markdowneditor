from funcs.utilities import errors


class TreeHandler:
    def __init__(self, tree):
        self._tree = tree

    def recursive_get(self, node_id: str, node: dict = None) -> dict | None:
        if node is None:
            node = self._tree

        if node["node_id"] == node_id:
            return node
        for child in node["children"]:
            result = self.recursive_get(node_id, child)
            if result is not None:
                return result
        return None

    def get_parent_node(self, node_id: str, node: dict = None) -> dict | None:
        if node is None:
            node = self._tree

        for child in node["children"]:
            if child["node_id"] == node_id:
                return node

            result = self.get_parent_node(node_id, child)
            if result is not None:
                return result

        return None

    def get_children_ids(self, node_id: str) -> list[str]:
        target = self.recursive_get(node_id)
        if not target:
            raise errors.NotFoundError("TreeHandler.not_found")

        result = []

        def collect(node: dict):
            for child in node["children"]:
                result.append(child["node_id"])
                collect(child)

        collect(target)
        return result

    def insert_node(self, parent_id: str, new_node: dict):
        parent_node = self.recursive_get(parent_id)
        if parent_node is None:
            raise errors.NotFoundError("TreeHandler.not_found")

        parent_node["children"].append(new_node)

    def move_node(self, parent_id: str, node_id: str):
        target_node = self.recursive_get(node_id)
        parent_node = self.recursive_get(parent_id)
        if target_node is None or parent_node is None:
            raise errors.NotFoundError("TreeHandler.not_found")

        if self.recursive_get(parent_id, target_node) is not None:
            raise errors.ForbiddenError("TreeHandler.cant_move_to_children")

        self.del_node(node_id)
        parent_node["children"].append(target_node)

    def update_node_label(self, node_id: str, label: dict):
        node = self.recursive_get(node_id)
        if node is None:
            raise errors.NotFoundError("TreeHandler.not_found")

        node["label"] = label

    def del_node(self, node_id: str):
        parent_node = self.get_parent_node(node_id)
        if not parent_node:
            raise errors.NotFoundError("TreeHandler.not_found")

        children: list = parent_node["children"]
        for i, child in enumerate(children):
            if child["node_id"] == node_id:
                del children[i]
                return

    def sort_tree(self, tree: dict | None = None) -> dict:
        if tree is None:
            tree = self._tree

        def sort_key(child: dict):
            is_file = not child["children"]
            return (is_file, child["label"])

        children: list = tree["children"]
        children.sort(key=sort_key)

        for child in children:
            self.sort_tree(child)

        return tree
