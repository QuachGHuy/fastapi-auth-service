from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1 import user, auth 
from app.db.session import engine
from app.db.base import Base

from app.models.user import User
from app.models.apikey import APIKey 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all) 
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Server started successfully"}