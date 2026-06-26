from fastapi import FastAPI
from contextlib import asynccontextmanager
import sys
import os
import importlib.util
import logging

# Execute local logging/logger.py without shadowing stdlib
logger_path = os.path.join(os.path.dirname(__file__), "logging", "logger.py")
spec = importlib.util.spec_from_file_location("init_logger", logger_path)
init_logger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(init_logger)

logger = logging.getLogger("jsl_app")

from config.settings import get_settings
from middleware.error_handler import setup_exception_handlers
from app.api.health import router as health_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Sequence
    settings = get_settings()
    logger.info(f"Starting {settings.app_name} in {settings.environment} mode.")
    logger.info("Initializing dependency container placeholders...")
    # Initialize DB connections here in the future
    yield
    # Shutdown Sequence
    logger.info(f"Shutting down {settings.app_name} cleanly.")
    # Close DB connections here in the future

def create_app() -> FastAPI:
    """Application Factory Pattern"""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        description="Enterprise Backend Foundation for JSL Process Contingency",
        version="1.0.0",
        lifespan=lifespan,
    )
    
    # Setup Centralized Exception Handling
    setup_exception_handlers(app)
    
    # Register Routers
    app.include_router(health_router, prefix=settings.api_v1_prefix, tags=["Health"])
    
    return app

app = create_app()
