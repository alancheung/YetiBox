import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from constants import LOCAL_HOST_IP, PORT

# Initialize the application
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:58369"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/data")
def get_data():
    return "Some Data!"

if __name__ == "__main__":
    uvicorn.run("main:app", host=LOCAL_HOST_IP, port=PORT, reload=True)