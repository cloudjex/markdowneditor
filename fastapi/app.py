import json
import logging

from mangum import Mangum
from starlette.responses import Response

import schema
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from funcs import (func_nodes, func_signin, func_signout, func_signup,
                   func_signup_verify, func_tree, func_tree_node,
                   func_tree_node_label, func_tree_node_move, func_users)
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
        403: {"description": "ForbiddenError"},
    },
)
async def func_signin_post(req: schema.SignInReq):
    return func_signin.post(req.email, req.password)


@app.post(
    path="/api/signup",
    tags=["Auth"],
    summary="Sign up",
    response_model=schema.ResultRes,
    responses={
        409: {"description": "ConflictError"},
    },
)
async def func_signup_post(req: schema.SignUpReq):
    return func_signup.post(req.email, req.password)


@app.post(
    path="/api/signup/verify",
    tags=["Auth"],
    summary="Email verification",
    response_model=schema.ResultRes,
    responses={
        401: {"description": "UnauthorizedError"},
        404: {"description": "NotFoundError"},
    },
)
async def func_signup_verify_post(req: schema.SignUpVerifyReq):
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
async def func_signout_post(jwt: dict = Depends(verify_token)):
    return func_signout.post()


@app.get(
    path="/api/users/me",
    tags=["User"],
    summary="Get your user info",
    response_model=schema.UserGetReq,
    responses={
        401: {"description": "UnauthorizedError"},
        404: {"description": "NotFoundError"},
    },
)
async def func_users_get(jwt: dict = Depends(verify_token)):
    return func_users.get(jwt["email"])


@app.get(
    path="/api/tree",
    tags=["Tree"],
    summary="Get tree",
    response_model=schema.Tree,
    responses={
        401: {"description": "UnauthorizedError"},
        404: {"description": "NotFoundError"},
    },
)
async def func_tree_get(jwt: dict = Depends(verify_token)):
    return func_tree.get(jwt["email"])


@app.post(
    path="/api/tree/node",
    tags=["Tree"],
    summary="Update tree, Insert node",
    response_model=schema.Tree,
    responses={
        401: {"description": "UnauthorizedError"},
        404: {"description": "NotFoundError"},
    },
)
async def func_tree_node_post(req: schema.TreeNodePostReq, jwt: dict = Depends(verify_token),):
    return func_tree_node.post(jwt["email"], req.parent_id, req.label)


@app.delete(
    path="/api/tree/node/{node_id}",
    tags=["Tree"],
    summary="Update tree, Delete node",
    response_model=schema.Tree,
    responses={
        401: {"description": "UnauthorizedError"},
        403: {"description": "ForbiddenError"},
        404: {"description": "NotFoundError"},
    },
)
async def func_tree_node_delete(node_id: str, jwt: dict = Depends(verify_token)):
    return func_tree_node.delete(jwt["email"], node_id)


@app.put(
    path="/api/tree/node/label/{node_id}",
    tags=["Tree"],
    summary="Update tree, Update label of node",
    response_model=schema.Tree,
    responses={
        401: {"description": "UnauthorizedError"},
        404: {"description": "NotFoundError"},
    },
)
async def func_tree_node_label_put(node_id: str, req: schema.TreeNodeLabelPutReq, jwt: dict = Depends(verify_token),):
    return func_tree_node_label.put(jwt["email"], node_id, req.label)


@app.put(
    path="/api/tree/node/move/{node_id}",
    tags=["Tree"],
    summary="Update tree, Move node",
    response_model=schema.Tree,
    responses={
        401: {"description": "UnauthorizedError"},
        403: {"description": "ForbiddenError"},
        404: {"description": "NotFoundError"},
    },
)
async def func_tree_node_move_put(node_id: str, req: schema.TreeNodeMovePutReq, jwt: dict = Depends(verify_token),):
    return func_tree_node_move.put(jwt["email"], node_id, req.parent_id)


@app.get(
    path="/api/nodes",
    tags=["Node"],
    summary="Get nodes",
    response_model=schema.NodesRes,
    responses={
        401: {"description": "UnauthorizedError"},
        404: {"description": "NotFoundError"},
    },
)
async def func_get_nodes(jwt: dict = Depends(verify_token)):
    return func_nodes.get(jwt["email"], None)


@app.get(
    path="/api/nodes/{node_id}",
    tags=["Node"],
    summary="Get node",
    response_model=schema.NodeRes,
    responses={
        401: {"description": "UnauthorizedError"},
        404: {"description": "NotFoundError"},
    },
)
async def func_get_node(node_id: str,  jwt: dict = Depends(verify_token)):
    return func_nodes.get(jwt["email"], node_id)


@app.put(
    path="/api/nodes/{node_id}",
    tags=["Node"],
    summary="Put node",
    response_model=schema.NodeRes,
    responses={
        401: {"description": "UnauthorizedError"},
        404: {"description": "NotFoundError"},
    },
)
async def func_update_nodes(node_id: str, req: schema.NodePutReq, jwt: dict = Depends(verify_token)):
    return func_nodes.put(jwt["email"], node_id, req.text)
