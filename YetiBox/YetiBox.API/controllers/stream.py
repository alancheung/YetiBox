import queue
import threading

import cv2
from fastapi import APIRouter, HTTPException, Request, status

import streamer

image_queue = queue.Queue(maxsize=1)
streamer = streamer.UsbStreamer(image_queue, streamer.OpenCvConfig(local_display=True))

router = APIRouter(prefix="/capture")
@router.get("/")
def get_status() -> str:
    ''' Return a string representing the status '''
    if not streamer.ready:
        return "Not Ready!"

    return "Running!"

@router.post("/start")
def start() -> None:
    # streamer = streamer.TestStreamer(image_queue)
    
    streamerThread = threading.Thread(target=streamer.run)
    streamerThread.start()

@router.get("/frame")
def get_frame(request: Request):
    ''' Display the last frame '''
    try:
        if not streamer.ready:
            return

        retObj = image_queue.get(block=True, timeout=3)
        
        cv2.imshow('FastAPI Frame', retObj)
        cv2.waitKey(1)
        return retObj
    except queue.Empty as ex:
        raise HTTPException(
            status_code=status.HTTPHTTP_500_INTERNAL_SERVER_ERROR,
            detail="Queue is empty!"
        )





