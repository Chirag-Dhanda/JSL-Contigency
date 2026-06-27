from typing import List, Optional, Literal, Union, Dict
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Interactive Components
# ---------------------------------------------------------

class KnowledgeCard(BaseModel):
    id: str
    title: str
    content: str
    is_safety_critical: bool = False

class QuickFact(BaseModel):
    id: str
    fact: str
    icon: Optional[str] = None

class SafetyAlert(BaseModel):
    id: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    message: str
    action_required: bool = False

class EngineeringTip(BaseModel):
    id: str
    tip: str
    technical_reference: Optional[str] = None

class ImportantWarning(BaseModel):
    id: str
    warning_text: str

class ExpandableSection(BaseModel):
    id: str
    header: str
    body_text: str

class Accordion(BaseModel):
    id: str
    sections: List[ExpandableSection]

# ---------------------------------------------------------
# Base Content Block
# ---------------------------------------------------------

class BaseContentBlock(BaseModel):
    id: str
    order: int

# ---------------------------------------------------------
# Specific Content Blocks
# ---------------------------------------------------------

class HeadingBlock(BaseContentBlock):
    type: Literal["HEADING"] = "HEADING"
    text: str
    level: int = 1 # e.g., H1, H2

class ParagraphBlock(BaseContentBlock):
    type: Literal["PARAGRAPH"] = "PARAGRAPH"
    text: str

class RichTextBlock(BaseContentBlock):
    type: Literal["RICH_TEXT"] = "RICH_TEXT"
    html_content: str

class ImageBlock(BaseContentBlock):
    type: Literal["IMAGE"] = "IMAGE"
    url: str
    alt_text: str
    caption: Optional[str] = None

class ImageGalleryBlock(BaseContentBlock):
    type: Literal["IMAGE_GALLERY"] = "IMAGE_GALLERY"
    urls: List[str]

class VideoBlock(BaseContentBlock):
    type: Literal["VIDEO"] = "VIDEO"
    url: str
    duration_secs: int

class PDFViewerBlock(BaseContentBlock):
    type: Literal["PDF_VIEWER"] = "PDF_VIEWER"
    url: str

class TableBlock(BaseContentBlock):
    type: Literal["TABLE"] = "TABLE"
    headers: List[str]
    rows: List[List[str]]

class TimelineBlock(BaseContentBlock):
    type: Literal["TIMELINE"] = "TIMELINE"
    events: List[Dict[str, str]] # e.g., [{"time": "10:00", "event": "Started"}]

class FlowDiagramBlock(BaseContentBlock):
    type: Literal["FLOW_DIAGRAM"] = "FLOW_DIAGRAM"
    diagram_data: str # JSON or Mermaid format

class EquipmentDiagramBlock(BaseContentBlock):
    type: Literal["EQUIPMENT_DIAGRAM"] = "EQUIPMENT_DIAGRAM"
    image_url: str
    clickable_components: List[str]

class ProcessAnimationBlock(BaseContentBlock):
    type: Literal["PROCESS_ANIMATION"] = "PROCESS_ANIMATION"
    animation_url: str

class CodeBlock(BaseContentBlock):
    type: Literal["CODE"] = "CODE"
    code: str
    language: str

class InteractiveSimulationBlock(BaseContentBlock):
    type: Literal["INTERACTIVE_SIMULATION"] = "INTERACTIVE_SIMULATION"
    simulation_id: str

class AIDiscussionBlock(BaseContentBlock):
    type: Literal["AI_DISCUSSION"] = "AI_DISCUSSION"
    prompt_context: str

# ---------------------------------------------------------
# The Union Type
# ---------------------------------------------------------

ContentBlock = Union[
    HeadingBlock,
    ParagraphBlock,
    RichTextBlock,
    ImageBlock,
    ImageGalleryBlock,
    VideoBlock,
    PDFViewerBlock,
    TableBlock,
    TimelineBlock,
    FlowDiagramBlock,
    EquipmentDiagramBlock,
    ProcessAnimationBlock,
    CodeBlock,
    InteractiveSimulationBlock,
    AIDiscussionBlock
]
