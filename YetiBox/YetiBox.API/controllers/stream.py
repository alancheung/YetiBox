from contextlib import asynccontextmanager
import queue
import threading

import cv2
from fastapi import APIRouter, FastAPI, HTTPException, Request, Response, status

import streamer

image_queue = queue.Queue(maxsize=1)
streamer = streamer.UsbStreamer(image_queue, streamer.OpenCvConfig(local_display=True))

@asynccontextmanager
async def lifespan(app: FastAPI):
    ''' FastAPI lifespan to handle multiprocess threading '''
    yield

router = APIRouter(prefix="/capture")

@router.get("/")
def get_status() -> str:
    ''' Return a string representing the status '''
    if not streamer.ready:
        return "Not Ready!"

    return "Running!"

@router.post("/start")
def start() -> None:
    ''' Start the camera stream '''
    # streamer = streamer.TestStreamer(image_queue)
    
    streamerThread = threading.Thread(target=streamer.run)
    streamerThread.start()

@router.post("/stop")
def start() -> None:
    if not streamer.ready:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Camera is not ready!")


@router.get("/frame")
def get_frame(request: Request) -> Response:
    ''' Display the last frame '''
    try:
        if not streamer.ready:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Camera is not ready!")

        qObj = image_queue.get(block=True, timeout=3)
        
        cv2.imshow('FastAPI Frame', qObj)
        cv2.waitKey(1)

        success, encoded_image = cv2.imencode('.jpg', qObj)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to encode image frame")

        return Response(content=encoded_image.tobytes(), media_type="image/jpeg")
    except queue.Empty as ex:
        raise HTTPException(status_code=status.HTTPHTTP_500_INTERNAL_SERVER_ERROR, detail="Queue is empty!")





