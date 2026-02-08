class User:
    def __init__(self, email: str, password: str, user_groups: list, options: dict):
        self.email = email
        self.password = password
        self.user_groups = user_groups
        self.options = Options(
            options["enabled"],
            options["otp"],
        )

    def to_dict(self, include_pw=False):
        return {
            "email": self.email,
            "password": self.password if include_pw else "***",
            "user_groups": self.user_groups,
            "options": self.options.to_dict(),
        }


class Options:
    def __init__(self, enabled: bool, otp: str):
        self.enabled = enabled
        self.otp = otp

    def to_dict(self):
        return {
            "enabled": self.enabled,
            "otp": self.otp,
        }
