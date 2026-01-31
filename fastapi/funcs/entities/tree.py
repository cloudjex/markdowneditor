class TreeInfo:
    def __init__(self, email: str, tree: dict):
        self.email = email
        self.tree = Tree(
            tree["node_id"],
            tree["label"],
            tree["children"]
        )

    def to_dict(self):
        return {
            "email": self.email,
            "tree": self.tree.to_dict(),
        }


class Tree:
    def __init__(self, node_id: str, label: str, children: list):
        self.node_id = node_id
        self.label = label
        self.children = [
            Tree(c["node_id"], c["label"], c["children"],) for c in children
        ]

    def to_dict(self):
        children = [i.to_dict() for i in self.children]
        return {
            "node_id": self.node_id,
            "label": self.label,
            "children": children,
        }
