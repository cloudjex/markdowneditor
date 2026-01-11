class BaseExceptionClass(Exception):
    status_code: int = None
    exception: str = None
    error_code: str = None

    def __init__(self, error_code: str):
        self.error_code = error_code


class BadRequestError(BaseExceptionClass):
    status_code = 400
    exception = "BAD_REQUEST"


class UnauthorizedError(BaseExceptionClass):
    status_code = 401
    exception = "UNAUTHORIZED"


class ForbiddenError(BaseExceptionClass):
    status_code = 403
    exception = "FORBIDDEN"


class NotFoundError(BaseExceptionClass):
    status_code = 404
    exception = "NOT_FOUND"


class ConflictError(BaseExceptionClass):
    status_code = 409
    exception = "CONFLICT"


class InternalServerError(BaseExceptionClass):
    status_code = 500
    exception = "INTERNAL_SERVER_ERROR"
