import os
from fastapi import APIRouter, Depends
from config.settings import get_settings, Settings
from logging import getLogger
import sys

# Using relative path from the app module to avoid absolute issues for now
# We will just import logging directly
import logging
logger = logging.getLogger("jsl_app")

router = APIRouter()

@router.get("/health", summary="Health Check")
async def health_check(settings: Settings = Depends(get_settings)):
    logger.info("Health check endpoint accessed.")
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "environment": settings.environment,
        "python_version": sys.version
    }
