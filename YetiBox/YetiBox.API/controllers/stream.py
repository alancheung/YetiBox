from contextlib import asynccontextmanager
import multiprocessing as mp
import queue
import threading

import cv2
from fastapi import APIRouter, FastAPI, HTTPException, Request, Response, status

import camera


raw_queue = mp.Queue(maxsize=1)
# A collection for the last processed frame from the camera. A processed frame is one in which any classifications have already run
processed_queue = mp.Queue(maxsize=1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    ''' FastAPI lifespan to handle multiprocess threading '''
    app.camera_worker = camera.CameraWorker(config=camera.CameraConfig(local_display=True), raw_queue=raw_queue, processed_queue=processed_queue)
    
    yield # let rest of program run

    if app.camera_worker.is_alive():
        print("Forcing class worker process termination...")
        app.camera_worker.terminate()

router = APIRouter(prefix="/capture")

@router.get("/")
def get_status() -> str:
    pass

@router.post("/start")
def start(request: Request) -> None:
    ''' Start the camera stream '''
    request.app.camera_worker.start()
    return

@router.post("/stop")
def start() -> None:
    pass


@router.get("/frame")
def get_frame(request: Request) -> Response:
    ''' Display the last frame '''
    try:
        try:
            qObj = raw_queue.get(block=True, timeout=3)
        except queue.Empty:
            return Response(status_code=status.HTTP_204_NO_CONTENT, detail="No data available in queue!");
        
        cv2.imshow('FastAPI Frame', qObj)
        cv2.waitKey(1)

        success, encoded_image = cv2.imencode('.jpg', qObj)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to encode image frame")

        return Response(content=encoded_image.tobytes(), media_type="image/jpeg")
    except BaseException as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Exception! {ex}")





