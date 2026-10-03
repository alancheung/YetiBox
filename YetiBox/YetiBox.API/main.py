import cv2
import queue
import threading
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from constants import *
import streamer
import controllers

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:58369"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(controllers.stream_router)

if __name__ == "__main__":
    uvicorn.run(app, host=LOCAL_HOST_IP, port=PORT)