from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from asgi_correlation_id import CorrelationIdMiddleware
from contextlib import asynccontextmanager
from database import database
from routers.post import router as post_router
from logging_conf import configure_logging
import logging
from routers.users import router as users_router

__name__="storeapi.main"
logger=logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app:FastAPI):
    configure_logging()
    logger.info("Hello World")
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)

@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request,exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request,exc)

@app.get('/')
async def root():
    return {"message": "Welcome to the Store API!"}
app.include_router(post_router)
app.include_router(users_router)