"""
EP-15: Full Regression Test Suite for EKOS v1.0
Covers all 14 Execution Package domains.

Run with:
    pytest tests/test_regression.py -v
"""
import pytest
import importlib
import sys
import os

# Ensure backend is on PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ══════════════════════════════════════════════════════════════════════════════
# EP-01: Infrastructure & DI Container
# ══════════════════════════════════════════════════════════════════════════════

class TestEP01_Infrastructure:
    def test_di_container_importable(self):
        """The core DI container must be importable without errors."""
        from core.di import container
        assert container is not None

    def test_config_manager_importable(self):
        from config.manager import get_config
        assert get_config is not None


# ══════════════════════════════════════════════════════════════════════════════
# EP-02: Metadata Engine
# ══════════════════════════════════════════════════════════════════════════════

class TestEP02_MetadataEngine:
    def test_metadata_models_importable(self):
        from modules.metadata_engine.models import MetadataObject
        assert MetadataObject is not None

    def test_metadata_service_importable(self):
        from modules.metadata_engine.service import MetadataEngineService
        assert MetadataEngineService is not None


# ══════════════════════════════════════════════════════════════════════════════
# EP-03: Ontology Engine
# ══════════════════════════════════════════════════════════════════════════════

class TestEP03_OntologyEngine:
    def test_ontology_models_importable(self):
        from modules.ontology.models import OntologyRelationship
        assert OntologyRelationship is not None

    def test_relationship_registry_importable(self):
        from modules.relationship_registry.service import RelationshipRegistryService
        assert RelationshipRegistryService is not None


# ══════════════════════════════════════════════════════════════════════════════
# EP-04: Knowledge Platform
# ══════════════════════════════════════════════════════════════════════════════

class TestEP04_KnowledgePlatform:
    def test_knowledge_platform_module_importable(self):
        from modules.knowledge_platform.module import KnowledgePlatformModule
        assert KnowledgePlatformModule is not None

    def test_knowledge_platform_api_importable(self):
        from modules.knowledge_platform.api import router
        assert router is not None


# ══════════════════════════════════════════════════════════════════════════════
# EP-05/07: Workflow Engine
# ══════════════════════════════════════════════════════════════════════════════

class TestEP05_WorkflowEngine:
    def test_workflow_models_importable(self):
        from modules.workflow_engine.models import WorkflowDefinition
        assert WorkflowDefinition is not None

    def test_workflow_module_importable(self):
        from modules.workflow_engine.module import WorkflowEngineModule
        assert WorkflowEngineModule is not None

    def test_workflow_api_importable(self):
        from modules.workflow_engine.api import router
        assert router is not None


# ══════════════════════════════════════════════════════════════════════════════
# EP-06: Search Engine
# ══════════════════════════════════════════════════════════════════════════════

class TestEP06_SearchEngine:
    def test_search_engine_module_importable(self):
        from modules.search_engine.module import SearchEngineModule
        assert SearchEngineModule is not None

    def test_search_engine_api_importable(self):
        from modules.search_engine.api import router
        assert router is not None


# ══════════════════════════════════════════════════════════════════════════════
# EP-08: AI Orchestration Platform
# ══════════════════════════════════════════════════════════════════════════════

class TestEP08_AIPlatform:
    def test_ai_platform_module_importable(self):
        from modules.ai_platform.module import AIOrchestrationModule
        assert AIOrchestrationModule is not None

    def test_ai_platform_api_importable(self):
        from modules.ai_platform.api import router
        assert router is not None


# ══════════════════════════════════════════════════════════════════════════════
# EP-09: Governance Platform
# ══════════════════════════════════════════════════════════════════════════════

class TestEP09_GovernancePlatform:
    def test_governance_engine_importable(self):
        from modules.governance_platform.governance_engine import GovernanceEngine
        assert GovernanceEngine is not None

    def test_governance_models_importable(self):
        from modules.governance_platform.models import GovernanceReviewPackage, GovernanceChangeType
        assert GovernanceReviewPackage is not None

    def test_governance_api_importable(self):
        from modules.governance_platform.api import router
        assert router is not None


# ══════════════════════════════════════════════════════════════════════════════
# EP-10: Integration Platform
# ══════════════════════════════════════════════════════════════════════════════

class TestEP10_IntegrationPlatform:
    def test_integration_platform_module_importable(self):
        from modules.integration_platform.module import IntegrationPlatformModule
        assert IntegrationPlatformModule is not None

    def test_integration_platform_api_importable(self):
        from modules.integration_platform.api import router
        assert router is not None


# ══════════════════════════════════════════════════════════════════════════════
# EP-11: Event Platform
# ══════════════════════════════════════════════════════════════════════════════

class TestEP11_EventPlatform:
    def test_event_bus_importable(self):
        from modules.events.bus import AdvancedEventBus
        assert AdvancedEventBus is not None

    def test_domain_event_model_importable(self):
        from modules.events.models import DomainEvent
        assert DomainEvent is not None

    def test_events_module_importable(self):
        from modules.events.module import EventPlatformModule
        assert EventPlatformModule is not None

    def test_events_api_importable(self):
        from modules.events.api import router
        assert router is not None


# ══════════════════════════════════════════════════════════════════════════════
# EP-12: Operations Platform
# ══════════════════════════════════════════════════════════════════════════════

class TestEP12_OperationsPlatform:
    def test_operations_module_importable(self):
        from modules.operations_platform.module import OperationsPlatformModule
        assert OperationsPlatformModule is not None

    def test_operations_api_importable(self):
        from modules.operations_platform.api import router
        assert router is not None


# ══════════════════════════════════════════════════════════════════════════════
# EP-13: Administration Platform
# ══════════════════════════════════════════════════════════════════════════════

class TestEP13_AdministrationPlatform:
    def test_administration_models_importable(self):
        from modules.administration_platform.models import ConfigurationSetting, FeatureFlag
        assert ConfigurationSetting is not None
        assert FeatureFlag is not None

    def test_config_manager_importable(self):
        from modules.administration_platform.config_manager import ConfigManager
        assert ConfigManager is not None

    def test_feature_manager_importable(self):
        from modules.administration_platform.feature_flags import FeatureManager
        assert FeatureManager is not None

    def test_review_center_importable(self):
        from modules.administration_platform.review_center import ReviewCenter
        assert ReviewCenter is not None

    def test_administration_module_importable(self):
        from modules.administration_platform.module import AdministrationPlatformModule
        assert AdministrationPlatformModule is not None

    def test_administration_api_importable(self):
        from modules.administration_platform.api import router
        assert router is not None


# ══════════════════════════════════════════════════════════════════════════════
# EP-14: Resilience Platform
# ══════════════════════════════════════════════════════════════════════════════

class TestEP14_ResiliencePlatform:
    def test_circuit_breaker_importable(self):
        from modules.resilience.circuit_breaker import CircuitBreaker, CircuitState
        assert CircuitBreaker is not None

    def test_circuit_breaker_state_machine(self):
        from modules.resilience.circuit_breaker import CircuitBreaker, CircuitState
        cb = CircuitBreaker(name="test-cb", failure_threshold=3)
        assert cb.state == CircuitState.CLOSED
        # Trigger enough failures to open
        for _ in range(3):
            cb.record_failure()
        assert cb.state == CircuitState.OPEN

    def test_retry_decorator_importable(self):
        from modules.resilience.retry import retry_with_backoff
        assert retry_with_backoff is not None

    def test_timeout_decorator_importable(self):
        from modules.resilience.timeout import with_timeout
        assert with_timeout is not None

    def test_distributed_cache_importable(self):
        from core.cache import IDistributedCache, InMemoryDistributedCacheMock
        assert InMemoryDistributedCacheMock is not None

    @pytest.mark.asyncio
    async def test_distributed_cache_ttl(self):
        from core.cache import InMemoryDistributedCacheMock
        cache = InMemoryDistributedCacheMock()
        await cache.set("key1", "value1", ttl_seconds=3600)
        result = await cache.get("key1")
        assert result == "value1"
        await cache.delete("key1")
        result = await cache.get("key1")
        assert result is None

    def test_security_hardening_importable(self):
        from core.security_hardening import RateLimiter, sanitize_output
        assert RateLimiter is not None
        assert sanitize_output is not None

    def test_sanitize_output_scrubs_secrets(self):
        from core.security_hardening import sanitize_output
        data = {"username": "alice", "password": "secret123", "token": "abc.def.ghi"}
        result = sanitize_output(data)
        assert result["username"] == "alice"
        assert result["password"] == "[REDACTED]"
        assert result["token"] == "[REDACTED]"


# ══════════════════════════════════════════════════════════════════════════════
# End-to-End Integration: Core Data Flow
# ══════════════════════════════════════════════════════════════════════════════

class TestE2E_CoreDataFlow:
    def test_full_module_import_chain(self):
        """Verify that the full module chain from EP-01 to EP-14 is importable."""
        modules_to_check = [
            "core.di",
            "modules.metadata_engine.module",
            "modules.object_designer.module",
            "modules.ontology.module",
            "modules.knowledge_platform.module",
            "modules.search_engine.module",
            "modules.workflow_engine.module",
            "modules.ai_platform.module",
            "modules.governance_platform.module",
            "modules.integration_platform.module",
            "modules.events.module",
            "modules.operations_platform.module",
            "modules.administration_platform.module",
            "modules.resilience.circuit_breaker",
            "core.cache",
            "core.security_hardening",
        ]
        for module_path in modules_to_check:
            try:
                mod = importlib.import_module(module_path)
                assert mod is not None, f"{module_path} returned None"
            except Exception as e:
                pytest.fail(f"Module {module_path} failed to import: {e}")
