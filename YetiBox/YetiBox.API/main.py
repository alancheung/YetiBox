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

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/data")
def get_data():
    try:
        retObj = image_queue.get(block=True, timeout=3)
    except Exception as ex:
        retObj = ex
    return retObj

if __name__ == "__main__":
    # streamer = streamer.TestStreamer(image_queue)
    streamer = streamer.UsbStreamer(image_queue, streamer.UsbCameraConfig(local_display=True))

    streamerThread = threading.Thread(target=streamer.run)
    streamerThread.start()
    uvicorn.run(app, host=LOCAL_HOST_IP, port=PORT)