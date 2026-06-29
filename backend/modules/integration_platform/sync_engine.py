"""
Integration Synchronization Engine (EP-10).
Manages the lifecycle of synchronizing data between external systems and EKOS.
"""
import logging
import asyncio
from typing import Dict, Any, List

from .models import SyncMode, ConflictType
from .gateway import IntegrationGateway
from .transformation import TransformationEngine
from .conflict_engine import ConflictResolutionEngine

logger = logging.getLogger("Integration.SyncEngine")


class IntegrationSyncEngine:
    def __init__(
        self,
        gateway: IntegrationGateway,
        transformation: TransformationEngine,
        conflict_engine: ConflictResolutionEngine
    ):
        self._gateway = gateway
        self._transformation = transformation
        self._conflict = conflict_engine

    async def execute_sync(self, connector_id: str, mode: SyncMode, entity_type: str) -> Dict[str, Any]:
        """
        Executes a synchronization run for a specific entity type on a connector.
        """
        logger.info(f"Starting {mode.value} sync for {entity_type} on connector {connector_id}")
        
        results = {
            "records_fetched": 0,
            "records_transformed": 0,
            "records_persisted": 0,
            "conflicts": 0,
            "errors": 0
        }

        try:
            # 1. Fetch data via Gateway
            query = {"entity": entity_type, "sync_mode": mode.value}
            payloads = await self._gateway.execute_read(connector_id, query)
            results["records_fetched"] = len(payloads)

            # 2. Get Mappings
            mappings = self._transformation.get_mappings_for_connector(connector_id)
            entity_mapping = next((m for m in mappings if m.source_entity == entity_type), None)
            
            if not entity_mapping:
                logger.warning(f"No mapping found for {entity_type} on connector {connector_id}. Skipping transform.")
                return results

            # 3. Transform and Detect Conflicts
            for payload in payloads:
                try:
                    transformed_data = self._transformation.transform_inbound(payload.data, entity_mapping)
                    results["records_transformed"] += 1
                    
                    # 4. Persist (Mocked here - would call Entity Engine)
                    # We simulate a schema conflict randomly based on payload content for demonstration
                    if "MISSING_REQ" in payload.data.get("DESCRIPTION", ""):
                        self._conflict.report_conflict(
                            connector_id=connector_id,
                            conflict_type=ConflictType.SCHEMA_MISMATCH,
                            error_message="Required field missing in external payload",
                            external_id=payload.external_id,
                            payload=payload.data
                        )
                        results["conflicts"] += 1
                    else:
                        # Simulate successful save
                        results["records_persisted"] += 1

                except Exception as e:
                    self._conflict.report_conflict(
                        connector_id=connector_id,
                        conflict_type=ConflictType.TRANSFORM_FAILURE,
                        error_message=str(e),
                        external_id=payload.external_id,
                        payload=payload.data
                    )
                    results["conflicts"] += 1

            logger.info(f"Sync complete for {entity_type}: {results}")
            return results

        except Exception as e:
            logger.error(f"Fatal error during sync run: {e}")
            results["errors"] += 1
            return results
