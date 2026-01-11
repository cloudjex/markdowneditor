class Tree:
    def __init__(self, email: str, node_tree: dict):
        self.email = email
        self.node_tree = NodeTree(
            node_tree["id"],
            node_tree["label"],
            node_tree["children"]
        )

    def to_dict(self):
        return {
            "email": self.email,
            "trees": self.node_tree.to_dict(),
        }


class NodeTree:
    def __init__(self, id: str, label: str, children: list):
        self.id = id
        self.label = label
        self.children = [
            NodeTree(c["id"], c["label"], c["children"],) for c in children if c
        ]

    def to_dict(self):
        children = [i.to_dict() for i in self.children if i]
        return {
            "id": self.id,
            "label": self.label,
            "children": children,
        }
