class User:
    def __init__(self, email: str, password: str, options: dict):
        self.email = email
        self.password = password
        self.options = Options(
            options["enabled"],
            options["otp"],
            options["user_groups"],
        )

    def to_dict(self, include_pw=False):
        return {
            "email": self.email,
            "password": self.password if include_pw else "***",
            "options": self.options.to_dict(),
        }


class Options:
    def __init__(self, enabled: bool, otp: str, user_groups: list):
        self.enabled = enabled
        self.otp = otp
        self.user_groups = user_groups

    def to_dict(self):
        return {
            "enabled": self.enabled,
            "otp": self.otp,
            "user_groups": self.user_groups,
        }
