class User:
    def __init__(self, email: str, password: str, user_groups: list, options: dict):
        self.email = email
        self.password = password
        self.user_groups = [
            UserGroup(i["group_name"], i["role"])
            for i in user_groups
        ]
        self.options = Options(
            options["enabled"],
            options["otp"],
        )

    def to_dict(self, include_pw=False):
        return {
            "email": self.email,
            "password": self.password if include_pw else "***",
            "user_groups": [i.to_dict() for i in self.user_groups],
            "options": self.options.to_dict(),
        }


class UserGroup:
    def __init__(self, group_name: str, role: str):
        self.group_name = group_name
        self.role = role

    def to_dict(self):
        return {"group_name": self.group_name, "role": self.role}


class Options:
    def __init__(self, enabled: bool, otp: str):
        self.enabled = enabled
        self.otp = otp

    def to_dict(self):
        return {
            "enabled": self.enabled,
            "otp": self.otp,
        }
