class Node:
    def __init__(self, email: str, id: str, text: str):
        self._email = email
        self._id = id
        self._text = text

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def json(self):
        return {
            "email": self._email,
            "id": self._id,
            "text": self._text,
        }
