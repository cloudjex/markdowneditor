class Node:
    def __init__(self, user_group: str, node_id: str, text: str):
        self.user_group = user_group
        self.node_id = node_id
        self.text = text

    def to_dict(self) -> dict:
        return {
            "user_group": self.user_group,
            "node_id": self.node_id,
            "text": self.text,
        }
