class Tree:
    def __init__(self, email: str, node_tree: dict):
        self._email = email
        self._node_tree = NodeTree(node_tree)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def node_tree(self):
        return self._node_tree

    @node_tree.setter
    def node_tree(self, node_tree):
        self._node_tree = node_tree

    def to_dict(self):
        return {
            "email": self._email,
            "trees": self._node_tree.to_dict(),
        }

    def set_node_tree(self, node_tree: dict) -> None:
        self._node_tree = NodeTree(node_tree)


class NodeTree:
    def __init__(self, tree_item: dict):
        self._id: str = tree_item["id"]
        self._label: str = tree_item["label"]
        self._children = [
            NodeTree(c) for c in tree_item["children"] if c
        ]

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def children(self):
        return [i.to_dict() for i in self._children if i]

    @children.setter
    def children(self, children):
        self._children = children

    def to_dict(self):
        children = [i.to_dict() for i in self._children if i]
        return {
            "id": self._id,
            "label": self._label,
            "children": children,
        }
