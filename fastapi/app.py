import logging

from mangum import Mangum

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from lib import func_login, func_logout, func_nodes, func_trees

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


@app.api_route("/login", methods=["POST"])
async def handle_login(request: Request):
    params = await handle_request(request)
    res = func_login.main(params)
    return handle_response(res)


@app.api_route("/logout", methods=["POST"])
async def handle_trees(request: Request):
    params = await handle_request(request)
    res = func_logout.main(params)
    return handle_response(res)


@app.api_route("/trees", methods=["GET", "PUT"])
async def handle_trees(request: Request):
    params = await handle_request(request)
    res = func_trees.main(params)
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
