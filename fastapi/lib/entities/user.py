class User:
    def __init__(self, email: str, password: str, options: dict):
        self.email = email
        self.password = password
        self.options = Options(options)

    def set_options(self, options: dict) -> None:
        self.options = Options(options)

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password,
            "options": self.options.to_dict(),
        }


class Options:
    def __init__(self, options: dict):
        self.enabled = options["enabled"]
        self.otp = options.get("otp", "")

    def to_dict(self):
        return {
            "enabled": self.enabled,
            "otp": self.otp if self.otp else None,
        }
