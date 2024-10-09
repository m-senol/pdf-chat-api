from fastapi import FastAPI
from .routes import router as api_router

from .models import metadata
from sqlalchemy import create_engine
from .config import DATABASE_URL
from .db import database, engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    metadata.create_all(engine)
    await database.connect()

    yield

    # Shutdown tasks
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "PDF Chat API"}
