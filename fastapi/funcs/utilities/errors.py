import inspect


class BaseExceptionClass(Exception):
    error_code: str = None

    def __init__(self):
        frame = inspect.stack()[1]
        function = frame.function
        line = frame.lineno
        self.error_code = f"{function}#{line}"


class BadRequestError(BaseExceptionClass):
    pass


class UnauthorizedError(BaseExceptionClass):
    pass


class ForbiddenError(BaseExceptionClass):
    pass


class NotFoundError(BaseExceptionClass):
    pass


class ConflictError(BaseExceptionClass):
    pass
