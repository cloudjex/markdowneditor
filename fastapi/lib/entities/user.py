class User:
    def __init__(self, email: str, password: str, options: dict):
        self._email = email
        self._password = password
        self._options = Options(options)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        self._email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options):
        if options is dict:
            options = Options(options)
        self._options = options

    @property
    def json(self):
        return {
            "email": self._email,
            "password": self._password,
            "options": self._options.json,
        }


class Options:
    def __init__(self, options: dict):
        self._enabled = options["enabled"]
        self._otp = options.get("otp", "")

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        self._enabled = enabled

    @property
    def otp(self):
        return self._otp

    @otp.setter
    def otp(self, otp):
        self._otp = otp

    @property
    def json(self):
        return {
            "enabled": self._enabled,
            "otp": self._otp if self._otp else None,
        }
