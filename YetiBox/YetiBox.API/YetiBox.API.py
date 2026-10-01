from fastapi import FastAPI

# Initialize the application
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}