class BaseExceptionClass(Exception):
    error_code: str = None

    def __init__(self, error_code: str):
        self.error_code = error_code


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
