from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.models import Base
from app.db.database import engine
from app.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # run this on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created (if not already present)")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)