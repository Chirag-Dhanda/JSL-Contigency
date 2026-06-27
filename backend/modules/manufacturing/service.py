from typing import Dict, List
from .models import ManufacturingStation, DigitalFactoryJourney, EmployeeStationProgress, ManufacturingStage, ProcessFlow, FlowConnection
from .enums import ManufacturingStageType, FlowDirection
from exceptions.base import NotFoundException
from logging import getLogger

logger = getLogger("ManufacturingService")

class ManufacturingService:
    def __init__(self):
        self._stations: Dict[str, ManufacturingStation] = {}
        self._journeys: Dict[str, DigitalFactoryJourney] = {}
        self._progress: Dict[str, EmployeeStationProgress] = {}
        
    def register_station(self, station: ManufacturingStation) -> None:
        self._stations[station.id] = station
        
    def register_journey(self, journey: DigitalFactoryJourney) -> None:
        self._journeys[journey.id] = journey
        
    def get_station(self, station_id: str) -> ManufacturingStation:
        if station_id not in self._stations:
            raise NotFoundException(f"Manufacturing Station {station_id} not found.")
        return self._stations[station_id]
        
    def get_journey(self, journey_id: str) -> DigitalFactoryJourney:
        if journey_id not in self._journeys:
            raise NotFoundException(f"Digital Factory Journey {journey_id} not found.")
        return self._journeys[journey_id]
        
    def log_station_visit(self, user_id: str, station_id: str) -> EmployeeStationProgress:
        """Records an employee visiting a digital factory station."""
        key = f"{user_id}_{station_id}"
        if key not in self._progress:
            self._progress[key] = EmployeeStationProgress(
                user_id=user_id,
                station_id=station_id,
                visited=True
            )
        else:
            self._progress[key].visited = True
            
        logger.debug(f"User {user_id} visited manufacturing station {station_id}.")
        return self._progress[key]

    def build_default_stainless_steel_journey(self) -> DigitalFactoryJourney:
        """Scaffolds the standard 21-step manufacturing process for JSL."""
        
        # We will build a few mock stations to represent the full 21 steps.
        # EAF
        eaf = ManufacturingStation(
            id="st-eaf",
            name="Electric Arc Furnace (EAF)",
            description="The primary melting unit where scrap and raw materials are melted using electric arcs.",
            purpose="Melt raw materials to create liquid steel.",
            input_materials=["Steel Scrap", "Ferroalloys", "Lime"],
            output_materials=["Liquid Steel"],
            equipment=["Electrodes", "Furnace Shell", "Transformer"],
            safety_precautions=["High Voltage Hazard", "Extreme Heat", "Splash Protection"],
            quality_parameters=["Temperature", "Carbon Content"],
            common_problems=["Electrode Breakage", "Refractory Wear"],
            sap_work_center_id="WC-EAF-01"
        )
        
        # AOD
        aod = ManufacturingStation(
            id="st-aod",
            name="Argon Oxygen Decarburization (AOD)",
            description="A refining vessel where carbon is removed from the molten steel while retaining chromium.",
            purpose="Decarburization and refining of stainless steel.",
            input_materials=["Liquid Steel from EAF", "Argon Gas", "Oxygen Gas"],
            output_materials=["Refined Stainless Steel"],
            equipment=["AOD Vessel", "Tuyeres", "Gas Valve Stand"],
            safety_precautions=["Gas Leak Hazard", "Extreme Heat"],
            quality_parameters=["Carbon Level", "Chromium Level"],
            common_problems=["Tuyere Blockage"],
            sap_work_center_id="WC-AOD-01"
        )
        
        self.register_station(eaf)
        self.register_station(aod)
        
        journey = DigitalFactoryJourney(
            id="journey-ss-01",
            title="Stainless Steel Core Manufacturing Journey",
            stations=[eaf, aod]
        )
        
        self.register_journey(journey)
        return journey

class ManufacturingExplorerService:
    def __init__(self):
        self._stages: Dict[str, ManufacturingStage] = {}
        self._flows: Dict[str, ProcessFlow] = {}
        self._mock_populate()

    def _mock_populate(self):
        """Populate the 21 requested placeholder stages."""
        stages_data = [
            ("Raw Material Procurement", ManufacturingStageType.RAW_MATERIAL),
            ("Raw Material Inspection", ManufacturingStageType.INSPECTION),
            ("Scrap Yard", ManufacturingStageType.STORAGE),
            ("Raw Material Storage", ManufacturingStageType.STORAGE),
            ("Electric Arc Furnace (EAF)", ManufacturingStageType.MELTING),
            ("Argon Oxygen Decarburization (AOD)", ManufacturingStageType.REFINING),
            ("Ladle Refining Furnace (LRF)", ManufacturingStageType.REFINING),
            ("Continuous Casting Machine (CCM)", ManufacturingStageType.CASTING),
            ("Grinding", ManufacturingStageType.GRINDING),
            ("Hot Rolling Mill", ManufacturingStageType.ROLLING),
            ("Annealing", ManufacturingStageType.ANNEALING),
            ("Pickling", ManufacturingStageType.PICKLING),
            ("Cold Rolling Mill", ManufacturingStageType.ROLLING),
            ("Slitting", ManufacturingStageType.SLITTING),
            ("Cut To Length", ManufacturingStageType.FINISHING),
            ("Surface Finishing", ManufacturingStageType.FINISHING),
            ("Quality Inspection", ManufacturingStageType.INSPECTION),
            ("Packing", ManufacturingStageType.PACKING),
            ("Warehouse", ManufacturingStageType.STORAGE),
            ("Dispatch", ManufacturingStageType.DISPATCH),
            ("Customer Delivery", ManufacturingStageType.DISPATCH)
        ]
        
        stages = []
        for i, (name, stage_type) in enumerate(stages_data):
            stage = ManufacturingStage(
                id=f"stage_{i}",
                name=name,
                stage_type=stage_type,
                description=f"Process description for {name}",
                order_index=i
            )
            self._stages[stage.id] = stage
            stages.append(stage)
            
        # Mock connections
        for i in range(len(stages) - 1):
            stages[i].connections.append(FlowConnection(target_stage_id=stages[i+1].id, direction=FlowDirection.NEXT))
            stages[i+1].connections.append(FlowConnection(target_stage_id=stages[i].id, direction=FlowDirection.PREVIOUS))

        self._flows["main_flow"] = ProcessFlow(
            id="main_flow",
            name="Primary Manufacturing Flow",
            description="End to end manufacturing sequence.",
            stages=stages
        )

    def get_process_flow(self, flow_id: str = "main_flow") -> ProcessFlow:
        return self._flows.get(flow_id)

    def get_stage(self, stage_id: str) -> ManufacturingStage:
        return self._stages.get(stage_id)
