from fastapi import FastAPI

from app.api.user import router as user_router

app = FastAPI(
    title="MatkaSears API",
    version="1.0.0"
)

app.include_router(user_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to MatkaSears API",
        "status": "Running"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }