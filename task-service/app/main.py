from contextlib import asynccontextmanager
from fastapi import FastAPI
from . import db
from app.routes import tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield
    db.shutdown()

app = FastAPI(lifespan=lifespan)
app.include_router(tasks.router)