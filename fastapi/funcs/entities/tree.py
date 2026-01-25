class TreeInfo:
    def __init__(self, email: str, tree: dict):
        self.email = email
        self.tree = Tree(
            tree["id"],
            tree["label"],
            tree["children"]
        )

    def to_dict(self):
        return {
            "email": self.email,
            "tree": self.tree.to_dict(),
        }


class Tree:
    def __init__(self, id: str, label: str, children: list):
        self.id = id
        self.label = label
        self.children = [
            Tree(c["id"], c["label"], c["children"],) for c in children
        ]

    def to_dict(self):
        children = [i.to_dict() for i in self.children]
        return {
            "id": self.id,
            "label": self.label,
            "children": children,
        }
