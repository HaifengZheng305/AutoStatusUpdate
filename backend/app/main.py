from fastapi import FastAPI
from app.routes import example

app = FastAPI()

app.include_router(example.router)

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}