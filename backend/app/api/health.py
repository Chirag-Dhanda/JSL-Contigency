import os
from fastapi import APIRouter, Depends
from config.manager import get_config, ConfigManager
from logging import getLogger
import sys

import logging
logger = logging.getLogger("HealthAPI")

router = APIRouter()

@router.get("/health", summary="Health Check")
async def health_check(config: ConfigManager = Depends(get_config)):
    logger.info("Health check endpoint accessed.")
    return {
        "status": "healthy",
        "app_name": config.app.app_name,
        "environment": config.app.environment,
        "python_version": sys.version
    }
