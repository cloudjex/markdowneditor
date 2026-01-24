import logging

from mangum import Mangum

import schema
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from funcs import (func_nodes, func_signin, func_signout, func_signup,
                   func_signup_verify, func_trees, func_trees_operate)
from funcs.utilities import errors
from funcs.utilities.jwt_client import JwtClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
handler = Mangum(app)


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


async def verify_token(request: Request) -> dict:
    token = request.headers.get("Authorization", "")
    return JwtClient().verify_id_token(token)


# =============== API Endpoint ===============
@app.post("/api/signin")
async def handle_signin(req: schema.SignInRequest):
    return func_signin.post(req.email, req.password)


@app.post("/api/signup")
async def handle_signup(req: schema.SignUpRequest):
    return func_signup.post(req.email, req.password)


@app.post("/api/signup/verify")
async def handle_signup_verify(req: schema.SignUpVerifyRequest):
    return func_signup_verify.post(req.email, req.otp)


@app.post("/api/signout")
async def handle_signout(jwt: dict = Depends(verify_token)):
    return func_signout.post()


@app.get("/api/trees")
async def handle_trees(jwt: dict = Depends(verify_token)):
    return func_trees.get(jwt["email"])


@app.post("/api/trees/operate")
async def handle_trees_operate(req: schema.TreePostRequest, jwt: dict = Depends(verify_token)):
    return func_trees_operate.post(jwt["email"], req.parent_id, req.label)


@app.delete("/api/trees/operate")
async def handle_delete_tree(id: str, jwt: dict = Depends(verify_token)):
    return func_trees_operate.delete(jwt["email"], id)


@app.get("/api/nodes")
async def handle_get_nodes(id: str = None, jwt: dict = Depends(verify_token)):
    return func_nodes.get(jwt["email"], id)


@app.put("/api/nodes")
async def handle_update_nodes(req: schema.NodePutRequest, jwt: dict = Depends(verify_token)):
    return func_nodes.put(jwt["email"], req.id, req.text)
