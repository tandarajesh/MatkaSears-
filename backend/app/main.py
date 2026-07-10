from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.user import User

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MatkaSears API",
    version="1.0.0"
)


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