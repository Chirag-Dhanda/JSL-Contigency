# Future Roadmap

The Stage 4 Baseline establishes the core AI and security framework. The upcoming stages will integrate this foundation directly with live factory systems.

## Stage 5: Enterprise Database Integration
- Replace the in-memory mock repositories with a real relational database (PostgreSQL).
- Implement Alembic for schema migrations.
- Connect the Auth and Permission modules to live SQL tables.

## Stage 6: SAP ERP Integration
- Connect the `ManufacturingService` and `AI Orchestrator` to the corporate SAP system.
- Allow the AI to query live Work Orders, Inventory levels, and Maintenance schedules.

## Stage 7: SCADA, PLC & IoT Integration
- **Live Telemetry**: Connect the backend to the factory floor (OPC UA, MQTT).
- **Real-Time AI**: Upgrade the `MfgExpert` agent to analyze live sensor data (e.g., EAF temperature) to predict anomalies.
- **Digital Twin**: Expand the frontend to visualize the live status of the physical factory based on IoT data streams.
