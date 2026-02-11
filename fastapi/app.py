import json
import logging

from mangum import Mangum
from starlette.responses import Response

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import auth, node, tree, user
from utilities import errors

app = FastAPI(title="cloudjex.com", description="## OpenAPI for cloudjex.com")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth.router, prefix="/api")
app.include_router(router=node.router, prefix="/api")
app.include_router(router=tree.router, prefix="/api")
app.include_router(router=user.router, prefix="/api")
handler = Mangum(app)


# =============== Middleware ===============
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.middleware("http")
async def __log(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)

    try:
        body = await request.json()
    except:
        body = {}

    log_content = json.dumps(
        {
            "Url": request.url.path,
            "Method": request.method,
            "Header": dict(request.headers),
            "Params": dict(request.query_params),
            "Body": body,
        },
        indent=2,
        ensure_ascii=False,
    )
    logger.info(f"[REQUEST] {log_content}")

    response: Response = await call_next(request)

    resp_body = b"".join([chunk async for chunk in response.body_iterator])
    resp_text = resp_body.decode("utf-8")

    try:
        parsed = json.loads(resp_text)
    except:
        parsed = resp_text

    log_content = json.dumps(
        {
            "Header": dict(response.headers),
            "Body": parsed,
        },
        indent=2,
        ensure_ascii=False,
    )
    logger.info(f"[RESPONSE] {log_content}")

    return Response(
        content=resp_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )


# =============== Exception Hander ===============
@app.exception_handler(errors.BadRequestError)
async def exception_handler(_, exc: errors.BadRequestError):
    return JSONResponse(status_code=400, content={"detail": exc.error_code})


@app.exception_handler(errors.UnauthorizedError)
async def exception_handler(_, exc: errors.UnauthorizedError):
    return JSONResponse(status_code=401, content={"detail": exc.error_code})


@app.exception_handler(errors.ForbiddenError)
async def exception_handler(_, exc: errors.ForbiddenError):
    return JSONResponse(status_code=403, content={"detail": exc.error_code})


@app.exception_handler(errors.NotFoundError)
async def exception_handler(_, exc: errors.NotFoundError):
    return JSONResponse(status_code=404, content={"detail": exc.error_code})


@app.exception_handler(errors.ConflictError)
async def exception_handler(_, exc: errors.ConflictError):
    return JSONResponse(status_code=409, content={"detail": exc.error_code})
