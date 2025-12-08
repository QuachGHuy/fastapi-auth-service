import time
import logging

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import user, auth, apikey
from app.db.session import engine
from app.db.base import Base
from app.models.user import User
from app.models.apikey import APIKey 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("LIFESPAN STARTUP: Application starting up.")
    try:
        # async with engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.create_all) 
        logger.info("DATABASE: Connection established.")
    except Exception as e:
        logger.error(f"DATABASE ERROR: Failed to establish connection to the database. Error: {e}")
    yield
    logger.info("LIFESPAN SHUTDOWN: Application is shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000", "http://localhost:8000"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)

@app.middleware("http")
async def log_requests_and_time(request: Request, call_next):
    
    start_time = time.time()
    logger.info(f"REQUEST START | Method: {request.method} | Path: {request.url.path}")

    response = await call_next(request)

    process_time = time.time() - start_time
    
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    
    logger.info(
        f"REQUEST END | Status: {response.status_code} | "
        f"Time: {process_time:.4f}s | Path: {request.url.path}"
    )

    return response

app.include_router(user.router, prefix="/api/v1/users", tags=["User"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(apikey.router, prefix="/api/v1/keys", tags=["APIKey"])


@app.get("/")
async def root():
    return {"message": "Server started successfully"}