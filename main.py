import uuid

from http import HTTPStatus
from typing import Annotated

from constants import SupportFileFormat, ImageProcessStatus
from fastapi import FastAPI, Request, Path, Query
from fastapi.responses import JSONResponse
from response_simulator import ResponseSimulator, ResponseResult


app = FastAPI()
image_content = None
response_simulator = ResponseSimulator()


@app.post("/send")
async def send(request: Request) -> JSONResponse:
    uid = str(uuid.uuid4())
    params = await request.json()
    global image_content
    image_content = params["image"]
    response = {"uid": uid}
    response_simulator.save_record(uid, image_content)
    return JSONResponse(response, status_code=HTTPStatus.OK)


@app.get("/status/{uid}")
async def get_status(
    uid: Annotated[str, Path()],
    file_type: Annotated[SupportFileFormat, Query()] = SupportFileFormat.GLB,
) -> JSONResponse:
    print(f"Inner get_status code block, uid: {uid}, file_type: {file_type}")
    response_simulator.delete_record_by_expired_time()
    res = response_simulator.get_record(uid)
    match res.status:
        case ImageProcessStatus.PROCESSING:
            response = {"status": res.status, "model_base64": None}
        case ImageProcessStatus.COMPLETED:
            response = {"status": res.status, "model_base64": res.image_content}
        case _:
            raise ValueError(f"Unknown status: {res.status}")
    return JSONResponse(response, status_code=HTTPStatus.OK)
