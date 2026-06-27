import sys
from fastapi import FastAPI
from contextlib import asynccontextmanager

# 1. Logging Initialization
import os
import importlib.util
logger_path = os.path.join(os.path.dirname(__file__), "logging", "logger.py")
spec = importlib.util.spec_from_file_location("init_logger", logger_path)
init_logger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(init_logger)

import logging
logger = logging.getLogger("Application")

from config.manager import get_config
from config.validator import validate_config
from middleware.error_handler import setup_exception_handlers
from core.lifecycle import lifecycle

def create_app() -> FastAPI:
    # 2. Configuration Validation (Fail Fast)
    validate_config()
    config = get_config()

    # 3. Application Lifecycle Hooks
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup sequence
        logger.info(f"Starting {config.app.app_name} in {config.app.environment} mode.")
        
        # Register Business Modules
        from modules.auth import AuthModule
        from modules.users import UsersModule
        from modules.organization import OrganizationModule
        from modules.permissions import PermissionsModule
        from modules.authorization import AuthorizationModule
        from modules.security import SecurityModule
        from modules.sessions import SessionsModule
        from modules.account_management import AccountManagementModule
        from modules.policies import PoliciesModule
        from modules.audit import AuditModule
        from modules.events import EventsModule
        from modules.templates import TemplatesModule
        from modules.notifications import NotificationsModule
        from modules.access_request import AccessRequestModule
        
        from modules.validation import ValidationModule
        from modules.middleware import MiddlewareModule
        from modules.roadmap import RoadmapModule
        from modules.learning import LearningModule
        from modules.manufacturing import ManufacturingModule
        from modules.knowledge import KnowledgeModule
        from modules.vector_db.module import VectorDBModule
        from modules.index_management.module import IndexManagementModule
        from modules.embeddings.module import EmbeddingsModule
        from modules.synchronization.module import SynchronizationModule
        from modules.conversations.module import ConversationsModule
        from modules.metadata_engine.module import MetadataEngineModule
        
        lifecycle.register_module(SecurityModule)
        lifecycle.register_module(SessionsModule)
        lifecycle.register_module(AuthModule)
        lifecycle.register_module(UsersModule)
        lifecycle.register_module(OrganizationModule)
        lifecycle.register_module(PermissionsModule)
        lifecycle.register_module(AuthorizationModule)
        lifecycle.register_module(PoliciesModule)
        lifecycle.register_module(AccountManagementModule)
        lifecycle.register_module(AuditModule)
        lifecycle.register_module(EventsModule)
        lifecycle.register_module(TemplatesModule)
        lifecycle.register_module(NotificationsModule)
        lifecycle.register_module(AccessRequestModule)
        lifecycle.register_module(ValidationModule)
        lifecycle.register_module(MiddlewareModule)
        lifecycle.register_module(KnowledgeModule)
        lifecycle.register_module(LearningModule)
        lifecycle.register_module(ManufacturingModule)
        lifecycle.register_module(RoadmapModule)
        lifecycle.register_module(VectorDBModule)
        lifecycle.register_module(IndexManagementModule)
        lifecycle.register_module(EmbeddingsModule)
        lifecycle.register_module(SynchronizationModule)
        lifecycle.register_module(ConversationsModule)
        lifecycle.register_module(MetadataEngineModule)
        
        await lifecycle.startup()
        
        # Seed Enterprise Metadata (Temporary for Demo)
        try:
            from core.di import container
            from modules.metadata_engine.service import MetadataEngineService
            from modules.metadata_engine.demo_seeder import seed_enterprise_metadata
            engine = container.resolve(MetadataEngineService)
            seed_enterprise_metadata(engine)
        except Exception as e:
            logger.warning(f"Failed to seed demo metadata: {e}")
        
        yield # Run Application
        
        # Shutdown sequence
        await lifecycle.shutdown()

    # 4. Framework Instantiation
    app = FastAPI(
        title=config.app.app_name,
        description="JSL Enterprise Learning Platform API",
        version="1.0.0",
        docs_url="/api/docs" if config.app.debug else None,
        redoc_url="/api/redoc" if config.app.debug else None,
        openapi_url="/api/openapi.json" if config.app.debug else None,
        lifespan=lifespan
    )

    # 5. Route & Middleware Registration
    setup_exception_handlers(app)
    
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register Enterprise Security Middleware
    from modules.middleware import EnterpriseSecurityMiddleware
    app.add_middleware(EnterpriseSecurityMiddleware)
    
    from app.api.health import router as health_router
    from modules.auth import auth_router
    from modules.ai_router.api import router as ai_api_router
    from modules.metadata_engine.api import router as metadata_router
    
    app.include_router(health_router, prefix=config.app.api_v1_prefix, tags=["System"])
    app.include_router(auth_router, prefix=config.app.api_v1_prefix)
    app.include_router(ai_api_router, prefix=config.app.api_v1_prefix)
    app.include_router(metadata_router)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    config = get_config()
    uvicorn.run(
        "main:app", 
        host=config.server.host, 
        port=config.server.port, 
        reload=config.app.debug
    )
