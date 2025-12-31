class BaseExceptions(Exception):
    status_code: int = 500
    exception: str = "INTERNAL_SERVER_ERROR"


class BadRequestError(BaseExceptions):
    status_code = 400
    exception = "BAD_REQUEST"


class UnauthorizedError(BaseExceptions):
    status_code = 401
    exception = "UNAUTHORIZED"


class ForbiddenError(BaseExceptions):
    status_code = 403
    exception = "FORBIDDEN"


class NotFoundError(BaseExceptions):
    status_code = 404
    exception = "NOT_FOUND"


class ConflictError(BaseExceptions):
    status_code = 409
    exception = "CONFLICT"
