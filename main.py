from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")    
    yield
    # Shutting down
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(router.router)

# uvicorn main:app --host 0.0.0.0 --port 5500