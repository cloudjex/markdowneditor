class TreeHander:
    def __init__(self):
        pass

    def find_node(self, node_id: str, tree: dict) -> dict | None:
        if tree.get("id") == node_id:
            return tree

        for child in tree.get("children"):
            result = self.find_node(node_id, child)
            if result is not None:
                return result

        return None

    def find_children_ids(self, node_id: str, tree: dict) -> list[str]:
        target = self.find_node(node_id, tree)
        result = []
        if target is None:
            return result

        def collect(node: dict):
            for child in node.get("children"):
                result.append(child["id"])
                collect(child)

        collect(target)
        return result

    def sort_tree(self, tree: dict) -> dict:
        if not tree or not isinstance(tree, dict):
            return tree

        def sort_key(child: dict) -> tuple[bool, str]:
            node_id: str = child.get("id", "")
            is_file = "children" not in child or not child.get("children")
            return (is_file, node_id)

        children = tree.get("children")
        if isinstance(children, list):
            children.sort(key=sort_key)
            for child in children:
                self.sort_tree(child)
            tree["children"] = children

        return tree
