import cv2
import queue
import threading
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from constants import *
import streamer

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:58369"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
image_queue = queue.Queue(maxsize=1)
streamer = streamer.UsbStreamer(image_queue, streamer.OpenCvConfig(local_display=True))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/data")
def get_data():
    try:
        if not streamer.ready:
            return "Not Ready!"

        retObj = image_queue.get(block=True, timeout=3)
        
        cv2.imshow('FastAPI Frame', retObj)
        cv2.waitKey(1)
    except Exception as ex:
        return f"Exception! {ex}"
    return "Running!"

if __name__ == "__main__":
    # streamer = streamer.TestStreamer(image_queue)
    
    streamerThread = threading.Thread(target=streamer.run)
    streamerThread.start()
    uvicorn.run(app, host=LOCAL_HOST_IP, port=PORT)