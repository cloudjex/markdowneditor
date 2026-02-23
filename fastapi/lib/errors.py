import inspect


class BaseExceptionClass(Exception):
    def __init__(self):
        frame = inspect.stack()[1]

        self.error_code = f"{frame.filename}.{frame.function}#{frame.lineno}"


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
