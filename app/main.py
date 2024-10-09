from fastapi import FastAPI
from .routes import router as api_router

from .models import metadata
from .db import database, engine
from contextlib import asynccontextmanager

from .middleware import ErrorMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    metadata.create_all(engine)
    await database.connect()

    yield

    # Shutdown tasks
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.add_middleware(ErrorMiddleware)
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "PDF Chat API"}
