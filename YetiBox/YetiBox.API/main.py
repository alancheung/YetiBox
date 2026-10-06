from contextlib import AsyncExitStack, asynccontextmanager
from functools import lru_cache
import cv2
import queue
import threading
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import camera
import controllers
import settings
from homeassistant import HomeAssistantGateway

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncExitStack() as stack:
        app.settings = get_settings()
        app.ha_gateway = HomeAssistantGateway(base_url=app.settings.ha_config.url, token=app.settings.ha_config.token)
        await stack.enter_async_context(controllers.stream_lifespan(app))
        yield

@lru_cache
def get_settings():
    return settings.Settings()

app = FastAPI(lifespan=lifespan)
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
    applicationSettings = settings.Settings()
    listenOn = settings.LOCAL_HOST_IP

    if applicationSettings.accept_external_traffic:
        listenOn = settings.ALL_IP
        
    uvicorn.run(app, host=listenOn, port=applicationSettings.port)