import logging

from mangum import Mangum

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from lib import (func_nodes, func_signin, func_signout, func_signup,
                 func_signup_verify, func_trees, func_trees_operate)

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


@app.api_route("/signin", methods=["POST"])
async def handle_signin(request: Request):
    params = await handle_request(request)
    res = func_signin.main(params)
    return handle_response(res)


@app.api_route("/signout", methods=["POST"])
async def handle_signout(request: Request):
    params = await handle_request(request)
    res = func_signout.main(params)
    return handle_response(res)


@app.api_route("/signup", methods=["POST"])
async def handle_signup(request: Request):
    params = await handle_request(request)
    res = func_signup.main(params)
    return handle_response(res)


@app.api_route("/signup/verify", methods=["POST"])
async def handle_signup_verify(request: Request):
    params = await handle_request(request)
    res = func_signup_verify.main(params)
    return handle_response(res)


@app.api_route("/trees", methods=["GET"])
async def handle_trees(request: Request):
    params = await handle_request(request)
    res = func_trees.main(params)
    return handle_response(res)


@app.api_route("/trees/operate", methods=["PUT", "DELETE"])
async def handle_trees_operate(request: Request):
    params = await handle_request(request)
    res = func_trees_operate.main(params)
    return handle_response(res)


@app.api_route("/nodes", methods=["GET", "PUT"])
async def handle_nodes(request: Request):
    params = await handle_request(request)
    res = func_nodes.main(params)
    return handle_response(res)


async def handle_request(request: Request) -> dict:
    try:
        body = await request.json()
    except Exception:
        body = {}

    params = {
        "path": request.url.path,
        "method": request.method.upper(),
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "body": body,
    }

    logger.info(
        f"[Request]: {params['method']} {params['path']} | Query: {params['query_params']} | Body: {body}"
    )
    return params


def handle_response(res: dict) -> JSONResponse:
    logger.info(
        f"[Response]: {res['status_code']} | Body: {res['body']}"
    )
    return JSONResponse(
        status_code=res["status_code"],
        headers=res["headers"],
        content=res["body"]
    )
