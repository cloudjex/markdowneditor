from lib.utilities import errors


class Tree:
    def __init__(self, email: str, tree: dict):
        self._email = email
        self._tree = TreeItem(tree)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def tree(self):
        return self._tree

    @tree.setter
    def tree(self, tree):
        if type(tree) is dict:
            tree = TreeItem(tree)
        self._tree = tree

    @property
    def json(self):
        return {
            "email": self._email,
            "tree": self._tree.json,
        }


class TreeItem:
    def __init__(self, tree_item: dict):
        self._id: str = tree_item["id"]
        self._label: str = tree_item["label"]
        self._children = [
            TreeItem(c) for c in tree_item["children"] if c
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
        return [i.json for i in self._children if i]

    @children.setter
    def children(self, children):
        self._children = children

    @property
    def json(self):
        children = [i.json for i in self._children if i]
        return {
            "id": self._id,
            "label": self._label,
            "children": children,
        }
