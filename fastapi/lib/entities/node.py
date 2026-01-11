class Node:
    def __init__(self, email: str, id: str, text: str):
        self.email = email
        self.id = id
        self.text = text

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "id": self.id,
            "text": self.text,
        }
