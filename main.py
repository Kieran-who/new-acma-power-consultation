from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import router
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    if not os.getenv('API_KEY'):
        print("WARNING No API-KEY environment variable set")
    yield
    # Shutting down
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(router.router)

# uvicorn main:app --host 0.0.0.0 --port 5500