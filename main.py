from fastapi import FastAPI
from database import engine, Base
from routers import tasks

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Task Manager API",
    description="Backend API for Task Manager Application",
    version="1.0.0"
)

# Include task routes
from routers import tasks
app.include_router(tasks.router)


@app.get("/")
def home():

    return {
        "message": "Welcome to Task Manager API",
        "status": "Backend is running successfully"
    }
    