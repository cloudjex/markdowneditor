class Tree:
    def __init__(self, email: str, node_tree: dict):
        self.email = email
        self.node_tree = NodeTree(node_tree)

    def set_node_tree(self, node_tree: dict) -> None:
        self.node_tree = NodeTree(node_tree)

    def to_dict(self):
        return {
            "email": self.email,
            "trees": self.node_tree.to_dict(),
        }


class NodeTree:
    def __init__(self, tree_item: dict):
        self.id: str = tree_item["id"]
        self.label: str = tree_item["label"]
        self.children = [
            NodeTree(c) for c in tree_item["children"] if c
        ]

    def to_dict(self):
        children = [i.to_dict() for i in self.children if i]
        return {
            "id": self.id,
            "label": self.label,
            "children": children,
        }
