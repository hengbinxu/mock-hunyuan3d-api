import uuid

from http import HTTPStatus
from typing import Annotated

from enum import StrEnum
from fastapi import FastAPI, Request, Path, Query
from fastapi.responses import JSONResponse


class SupportFileFormat(StrEnum):
    GLB = "glb"
    OBJ = "obj"
    PLY = "ply"
    STL = "stl"


app = FastAPI()
image_content = None


@app.post("/send")
async def send(request: Request) -> JSONResponse:
    uid = str(uuid.uuid4())
    params = await request.json()
    global image_content
    image_content = params["image"]
    response = {"uid": uid}
    return JSONResponse(response, status_code=HTTPStatus.OK)


@app.get("/status/{uid}")
async def get_status(
    uid: Annotated[str, Path()],
    file_type: Annotated[SupportFileFormat, Query()] = SupportFileFormat.GLB,
) -> JSONResponse:
    print(f"Inner get_status code block, uid: {uid}, file_type: {file_type}")
    response = {"status": "completed", "model_base64": image_content}
    return JSONResponse(response, status_code=HTTPStatus.OK)
