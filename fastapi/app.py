import json
import logging

from mangum import Mangum
from starlette.responses import Response

import schema
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from funcs import (func_nodes, func_signin, func_signout, func_signup,
                   func_signup_verify, func_tree, func_tree_operate)
from funcs.utilities import errors
from funcs.utilities.jwt_client import JwtClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)


app = FastAPI(title="cloudjex.com", description="## OpenAPI for cloudjex.com")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
handler = Mangum(app)


# =============== Middleware ===============
@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)

    try:
        body = await request.json()
    except:
        body = {}

    log_content = json.dumps({
        "Url": request.url.path,
        "Method": request.method,
        "Header": dict(request.headers),
        "Params": dict(request.query_params),
        "Body": body,
    }, indent=2, ensure_ascii=False)
    logger.info(f"[REQUEST] {log_content}")

    response: Response = await call_next(request)

    resp_body = b"".join([chunk async for chunk in response.body_iterator])
    resp_text = resp_body.decode("utf-8")

    try:
        parsed = json.loads(resp_text)
    except:
        parsed = resp_text

    log_content = json.dumps({
        "Header": dict(response.headers),
        "Body": parsed,
    }, indent=2, ensure_ascii=False)
    logger.info(f"[RESPONSE] {log_content}")

    return Response(
        content=resp_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )


async def verify_token(request: Request) -> dict:
    token = request.headers.get("Authorization", "")
    return JwtClient().verify(token)


# =============== Exception Hander ===============
@app.exception_handler(errors.UnauthorizedError)
async def unauthorized_exception_handler(_, exc: errors.UnauthorizedError):
    return JSONResponse(status_code=401, content={"detail": exc.error_code})


@app.exception_handler(errors.ForbiddenError)
async def forbidden_exception_handler(_, exc: errors.ForbiddenError):
    return JSONResponse(status_code=403, content={"detail": exc.error_code})


@app.exception_handler(errors.NotFoundError)
async def notfound_exception_handler(_, exc: errors.NotFoundError):
    return JSONResponse(status_code=404, content={"detail": exc.error_code})


@app.exception_handler(errors.ConflictError)
async def conflict_exception_handler(_, exc: errors.ConflictError):
    return JSONResponse(status_code=409, content={"detail": exc.error_code})


# =============== API Endpoint ===============
@app.post(
    path="/api/signin",
    tags=["Auth"],
    summary="Sign in",
    response_model=schema.SignInRes,
    responses={
        401: {"description": "UnauthorizedError"},
    },
)
async def handle_signin(req: schema.SignInReq):
    return func_signin.post(req.email, req.password)


@app.post(
    path="/api/signup",
    tags=["Auth"],
    summary="Sign up",
    response_model=schema.ResultRes,
)
async def handle_signup(req: schema.SignUpReq):
    return func_signup.post(req.email, req.password)


@app.post(
    path="/api/signup/verify",
    tags=["Auth"],
    summary="Email verification",
    response_model=schema.ResultRes,
    responses={
        401: {"description": "UnauthorizedError"},
    },
)
async def handle_signup_verify(req: schema.SignUpVerifyReq):
    return func_signup_verify.post(req.email, req.otp)


@app.post(
    path="/api/signout",
    tags=["Auth"],
    summary="Sign out",
    response_model=schema.ResultRes,
    responses={
        401: {"description": "UnauthorizedError"},
    },
)
async def handle_signout(jwt: dict = Depends(verify_token)):
    return func_signout.post()


@app.get(
    path="/api/tree",
    tags=["Tree"],
    summary="Get tree",
    response_model=schema.Tree,
    responses={
        401: {"description": "UnauthorizedError"},
    },
)
async def handle_tree(jwt: dict = Depends(verify_token)):
    return func_tree.get(jwt["email"])


@app.post(
    path="/api/tree/operate",
    tags=["Tree"],
    summary="Update tree, Insert node",
    response_model=schema.Tree,
    responses={
        401: {"description": "UnauthorizedError"},
    },
)
async def handle_tree_operate(req: schema.TreePostReq, jwt: dict = Depends(verify_token),):
    return func_tree_operate.post(jwt["email"], req.parent_id, req.label)


@app.put(
    path="/api/tree/operate/{id}",
    tags=["Tree"],
    summary="Update tree, Update node",
    response_model=schema.Tree,
    responses={
        401: {"description": "UnauthorizedError"},
    },
)
async def handle_tree_operate(id, req: schema.TreePutReq, jwt: dict = Depends(verify_token),):
    return func_tree_operate.put(jwt["email"], id, req.label)


@app.delete(
    path="/api/tree/operate/{id}",
    tags=["Tree"],
    summary="Update tree, Delete node",
    response_model=schema.Tree,
    responses={
        401: {"description": "UnauthorizedError"},
    },
)
async def handle_delete_tree(id: str, jwt: dict = Depends(verify_token)):
    return func_tree_operate.delete(jwt["email"], id)


@app.get(
    path="/api/nodes",
    tags=["Node"],
    summary="Get nodes",
    response_model=schema.NodesRes,
    responses={
        401: {"description": "UnauthorizedError"},
    },
)
async def handle_get_nodes(jwt: dict = Depends(verify_token)):
    return func_nodes.get(jwt["email"], None)


@app.get(
    path="/api/nodes/{id}",
    tags=["Node"],
    summary="Get node",
    response_model=schema.NodeRes,
    responses={
        401: {"description": "UnauthorizedError"},
    },
)
async def handle_get_node(id: str,  jwt: dict = Depends(verify_token)):
    return func_nodes.get(jwt["email"], id)


@app.put(
    path="/api/nodes/{id}",
    tags=["Node"],
    summary="Put node",
    response_model=schema.NodeRes,
    responses={
        401: {"description": "UnauthorizedError"},
    },
)
async def handle_update_nodes(id: str, req: schema.NodePutReq, jwt: dict = Depends(verify_token)):
    return func_nodes.put(jwt["email"], id, req.text)
