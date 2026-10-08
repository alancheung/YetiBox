from contextlib import asynccontextmanager
import multiprocessing as mp
import queue
from collections.abc import Iterator

import cv2
from fastapi import APIRouter, FastAPI, Request, Response, status
from fastapi.responses import JSONResponse, StreamingResponse

from camera import CameraWorker
from settings import CameraConfig, Settings


raw_queue = mp.Queue(maxsize=1)
# A collection for the last processed frame from the camera. A processed frame is one in which any classifications have already run
processed_queue = mp.Queue(maxsize=1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ FastAPI lifespan to handle multiprocess threading """
    appSettings: Settings = app.settings
    gateway = app.ha_gateway

    app.camera_worker = CameraWorker(config=appSettings.camera_config, raw_queue=raw_queue, processed_queue=processed_queue, gateway=gateway)
    app.camera_worker.start()

    try:
        yield
    finally:
        if app.camera_worker.is_alive():
            print("Forcing class worker process termination...")
            app.camera_worker.terminate()
            app.camera_worker.join(timeout=1)

router = APIRouter(prefix="/capture")

@router.get("/")
def get_status(request: Request) -> JSONResponse:
    worker: CameraWorker = request.app.camera_worker
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"Worker": worker.is_alive()},
    )

@router.post("/start")
def start(request: Request) -> None:
    """
    Start the camera stream 
    TODO should use events for this
    """
    worker: CameraWorker = request.app.camera_worker

    if worker is None or not worker.is_alive():
        worker.kill() if worker is not None else _
        request.app.camera_worker = CameraWorker(config=request.app.settings.camera_config, raw_queue=raw_queue, processed_queue=processed_queue, gateway=requestapp.ha_gateway)
        request.app.camera_worker.start()
    pass

@router.post("/stop")
def stop() -> None:
    """
   Stop the camera stream 
   TODO should use events for this
    """
    pass

@router.get("/frame")
def get_frame(request: Request) -> Response:
    """ Display the last frame """
    try:
        frame = processed_queue.get(timeout=3)
    except queue.Empty:
        return Response(status_code=status.HTTP_204_NO_CONTENT, detail="No data available in queue!")

    encoded_frame = _encode_frame(frame)
    if encoded_frame is None:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(content=encoded_frame, media_type="image/jpeg")

@router.get("/stream")
def stream_frames() -> StreamingResponse:
    return StreamingResponse(
        _stream_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
    )

def _encode_frame(frame) -> bytes | None:
    success, encoded_frame = cv2.imencode(".jpg", frame)
    if not success:
        return None

    return encoded_frame.tobytes()

def _stream_frames() -> Iterator[bytes]:
    while True:
        try:
            frame = processed_queue.get(timeout=1)
        except queue.Empty:
            continue

        encoded_frame = _encode_frame(frame)
        if encoded_frame is None:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n"
            b"Content-Length: "
            + str(len(encoded_frame)).encode("ascii")
            + b"\r\n\r\n"
            + encoded_frame
            + b"\r\n"
        )