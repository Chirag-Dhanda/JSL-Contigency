"""
SAP Connector (EP-10).
Mock implementation of SAP connectivity (OData / RFC simulator).
"""
import asyncio
from typing import List, Dict, Any
from ..models import DataPayload
from ..sdk.base import BaseConnector, ConnectorContext


class SAPConnector(BaseConnector):
    @property
    def provider_name(self) -> str:
        return "SAP"

    async def connect(self, context: ConnectorContext) -> bool:
        context.logger.info("Initializing connection to SAP (Simulated)")
        # In a real scenario, initialize pyrfc or an OData client here
        await asyncio.sleep(0.5)
        return True

    async def health_check(self, context: ConnectorContext) -> bool:
        context.logger.debug("Pinging SAP system...")
        return True

    async def discover_schema(self, context: ConnectorContext) -> Dict[str, Any]:
        """Simulates fetching SAP OData metadata or RFC structures."""
        context.logger.info("Discovering SAP schema metadata")
        await asyncio.sleep(0.5)
        return {
            "entities": {
                "Equipment": {
                    "fields": {
                        "EQUI_ID": "string",
                        "DESCRIPTION": "string",
                        "STATUS": "string",
                        "PLANT_ID": "string"
                    }
                },
                "FunctionalLocation": {
                    "fields": {
                        "FLOC_ID": "string",
                        "DESCRIPTION": "string"
                    }
                }
            }
        }

    async def read(self, context: ConnectorContext, query: Dict[str, Any]) -> List[DataPayload]:
        """Simulates reading data from SAP."""
        entity_type = query.get("entity", "Unknown")
        context.logger.info(f"Reading {entity_type} from SAP")
        await asyncio.sleep(0.5)

        # Mock payload
        return [
            DataPayload(
                external_id="1000001",
                entity_type=entity_type,
                data={
                    "EQUI_ID": "1000001",
                    "DESCRIPTION": "Pump P-101",
                    "STATUS": "ACTIVE",
                    "PLANT_ID": "1000"
                }
            )
        ]

    async def write(self, context: ConnectorContext, payloads: List[DataPayload]) -> bool:
        """
        Write operations are structurally disabled in the mock.
        Even in production, the Gateway blocks this unless governed.
        """
        context.logger.warning("Attempted write to SAP. Write operations require governance review.")
        raise PermissionError("SAP write operations are not enabled by default.")
