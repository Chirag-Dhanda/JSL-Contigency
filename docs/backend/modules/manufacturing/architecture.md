# Manufacturing Domain Architecture

**Purpose**: Encapsulates the physical reality of the JSL Stainless Steel plant into a digital data contract, serving as the backbone for the Digital Factory Onboarding Journey.

## 1. Manufacturing Data Models (`modules/manufacturing/models.py`)

### `ManufacturingStation`
Represents a physical production unit (e.g., Electric Arc Furnace). It is deeply modeled to act as a central hub of knowledge:
- **Core Info**: `name`, `description`, `purpose`.
- **Material Flow**: `input_materials`, `output_materials`.
- **Engineering Data**: `equipment`, `safety_precautions`, `quality_parameters`.
- **Enterprise Hooks**: 
  - `sap_work_center_id`: Prepared for future SAP PP (Production Planning) integration.
  - `scada_endpoint`: Prepared for live telemetry data injection (e.g., furnace temperature).
  - `iot_sensors`: Prepared to link with localized sensor networks.

### `DigitalFactoryJourney`
A predefined sequence of `ManufacturingStation` models representing the 21-step steelmaking process.

### `EmployeeStationProgress`
Tracks employee engagement with the Digital Factory. Records stations visited and time spent absorbing the material.

## 2. Learning Module Integration (`modules/learning/models.py`)
To prevent the manufacturing domain from becoming bloated with multimedia content, the `LearningModule` has been extended:
- `StationLesson`: Links to a `ManufacturingStation` ID.
- `KnowledgeCard`: Contains bite-sized, interactive text (e.g., "Why is Argon used in AOD?").
- `InteractiveDiagram`: Holds the URL to complex SVG/Image diagrams where users can click individual machine components for detailed breakdowns.

## 3. Frontend Digital Twin (`frontend/modules/digital-factory/`)
The visual abstraction is built on a scalable HTML Canvas using CSS transforms.
- **Pan and Zoom**: Pure JavaScript mathematics tracks mouse dragging and scroll wheels to manipulate a massive `3000px by 2000px` div, simulating a blueprint interaction.
- **Process Flow**: SVG `<path>` elements trace the material flow between stations. Animated dash arrays simulate liquid/material moving through pipes.
- **Glassmorphic Data Modals**: When a user clicks a station, an absolute-positioned overlay renders the complex backend data (Inputs, Outputs, Safety) using premium glassmorphism styles and structured tabs.
