class Node:
    def __init__(self, email: str, node_id: str, text: str):
        self.email = email
        self.node_id = node_id
        self.text = text

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "node_id": self.node_id,
            "text": self.text,
        }
