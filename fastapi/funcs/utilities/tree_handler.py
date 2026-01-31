from funcs.utilities import errors


class TreeHandler:
    def __init__(self, tree):
        self._tree = tree

    def get_node(self, node_id: str) -> dict:
        def recursive(node: dict) -> dict | None:
            if node["node_id"] == node_id:
                return node
            for child in node["children"]:
                result = recursive(child)
                if result is not None:
                    return result
            return None

        result = recursive(self._tree)
        if result is None:
            raise errors.NotFoundError("TreeHandler.not_found")
        return result

    def get_parent_node(self, node_id: str) -> dict:
        def find_parent(node: dict) -> dict | None:
            for child in node["children"]:
                if child["node_id"] == node_id:
                    return node
                result = find_parent(child)
                if result is not None:
                    return result
            return None

        parent = find_parent(self._tree)
        if parent is None:
            raise errors.NotFoundError("TreeHandler.not_found")
        return parent

    def get_children_ids(self, node_id: str) -> list[str]:
        target = self.get_node(node_id)
        result = []

        def collect(node: dict):
            for child in node["children"]:
                result.append(child["node_id"])
                collect(child)

        collect(target)
        return result

    def insert_node(self, parent_id: str, new_node: dict):
        parent_node = self.get_node(parent_id)
        parent_children: list[dict] = parent_node["children"]
        parent_children.append(new_node)

    def move_node(self, parent_id: str, node_id: str):
        parent_node = self.get_node(parent_id)
        target_node = self.get_node(node_id)
        self.del_node(node_id)
        parent_node["children"].append(target_node)

    def update_node_label(self, node_id: str, label: dict):
        node = self.get_node(node_id)
        node["label"] = label

    def del_node(self, node_id: str):
        parent_node = self.get_parent_node(node_id)
        children: list = parent_node["children"]
        for i, child in enumerate(children):
            if child["node_id"] == node_id:
                del children[i]
                return
        raise errors.NotFoundError("TreeHandler.not_found")

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
