from contextlib import AsyncExitStack, asynccontextmanager
import cv2
import queue
import threading
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import constants
import camera
import controllers

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(controllers.stream_lifespan(app))
        yield

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:58369"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(controllers.stream_router)
app.include_router(controllers.decompiler_router)

if __name__ == "__main__":
    uvicorn.run(app, host=constants.LOCAL_HOST_IP, port=constants.PORT)