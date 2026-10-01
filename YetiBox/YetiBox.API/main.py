import os
import uvicorn

from fastapi import FastAPI

from constants import LOCAL_HOST_IP, PORT

# Initialize the application
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=LOCAL_HOST_IP, port=PORT, reload=True)