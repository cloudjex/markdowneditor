class User:
    def __init__(self, email: str, password: str, options: dict):
        self.email = email
        self.password = password
        self.options = Options(options)

    def to_dict(self, include_pw=False):
        return {
            "email": self.email,
            "password": self.password if include_pw else "***",
            "options": self.options.to_dict(),
        }


class Options:
    def __init__(self, options: dict):
        self.enabled: bool = options["enabled"]
        self.otp: str = options["otp"]

    def to_dict(self):
        return {
            "enabled": self.enabled,
            "otp": self.otp,
        }
