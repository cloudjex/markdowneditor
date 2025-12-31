class BaseExceptionClass(Exception):
    status_code: int = 500
    exception: str = "INTERNAL_SERVER_ERROR"


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
