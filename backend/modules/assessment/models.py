from typing import List, Optional, Literal, Annotated, Union, Dict
from pydantic import BaseModel, Field
from datetime import datetime

from .enums import QuestionType, AssessmentStatus, DifficultyLevel
from backend.modules.competency.enums import CompetencyArea

# ---------------------------------------------------------
# Question Bank Architecture
# ---------------------------------------------------------

class BaseQuestion(BaseModel):
    id: str
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    points: float = 1.0
    negative_points: float = 0.0
    mapped_competencies: List[CompetencyArea] = []
    learning_objective_id: Optional[str] = None
    
    # Features
    text: str
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    pdf_reference: Optional[str] = None
    diagram_url: Optional[str] = None
    hint: Optional[str] = None
    explanation: Optional[str] = None

class SingleChoiceQuestion(BaseQuestion):
    type: Literal["SINGLE_CHOICE"] = "SINGLE_CHOICE"
    options: List[str]
    correct_option_index: int

class MultipleChoiceQuestion(BaseQuestion):
    type: Literal["MULTIPLE_CHOICE"] = "MULTIPLE_CHOICE"
    options: List[str]
    correct_option_indices: List[int]
    allow_partial_marks: bool = False

class TrueFalseQuestion(BaseQuestion):
    type: Literal["TRUE_FALSE"] = "TRUE_FALSE"
    is_true: bool

class FillInBlankQuestion(BaseQuestion):
    type: Literal["FILL_IN_BLANK"] = "FILL_IN_BLANK"
    text_with_blanks: str # e.g., "The primary safety rule is [BLANK1]"
    correct_answers: Dict[str, str] # e.g., {"BLANK1": "PPE"}

class MatchingQuestion(BaseQuestion):
    type: Literal["MATCHING"] = "MATCHING"
    left_items: List[str]
    right_items: List[str]
    correct_pairs: Dict[str, str] # e.g., {"Left 1": "Right 2"}

class SequenceQuestion(BaseQuestion):
    type: Literal["SEQUENCE"] = "SEQUENCE"
    items_to_sequence: List[str]
    correct_sequence: List[str]

class HotspotQuestion(BaseQuestion):
    type: Literal["IMAGE_HOTSPOT"] = "IMAGE_HOTSPOT"
    target_regions: List[Dict[str, float]] # e.g., bounding boxes

class ScenarioQuestion(BaseQuestion):
    type: Literal["SCENARIO"] = "SCENARIO"
    scenario_text: str
    sub_questions: List["Question"] # Recursive support for sub questions

class ChecklistQuestion(BaseQuestion):
    type: Literal["CHECKLIST"] = "CHECKLIST"
    checklist_items: List[str]
    required_checked_indices: List[int]

class ProcessFlowQuestion(BaseQuestion):
    type: Literal["PROCESS_FLOW"] = "PROCESS_FLOW"
    flow_steps: List[str]
    correct_flow: List[str]

# Future placeholders
class AIOralQuestion(BaseQuestion):
    type: Literal["AI_ORAL"] = "AI_ORAL"
    prompt_context: str

class PracticalQuestion(BaseQuestion):
    type: Literal["PRACTICAL"] = "PRACTICAL"
    evaluation_rubric_id: str

Question = Annotated[Union[
    SingleChoiceQuestion,
    MultipleChoiceQuestion,
    TrueFalseQuestion,
    FillInBlankQuestion,
    MatchingQuestion,
    SequenceQuestion,
    HotspotQuestion,
    ScenarioQuestion,
    ChecklistQuestion,
    ProcessFlowQuestion,
    AIOralQuestion,
    PracticalQuestion
], Field(discriminator="type")]

ScenarioQuestion.model_rebuild()

# ---------------------------------------------------------
# Assessment Structure
# ---------------------------------------------------------

class Assessment(BaseModel):
    id: str
    title: str
    description: str
    difficulty: DifficultyLevel
    estimated_duration_mins: int
    passing_percentage: float = 80.0
    max_attempts: int = 1
    randomize_questions: bool = False
    randomize_answers: bool = False
    time_limit_mins: Optional[int] = None
    
    department: Optional[str] = None
    role: Optional[str] = None
    learning_module_id: Optional[str] = None
    prerequisites: List[str] = [] # list of assessment IDs
    
    questions: List[Question]

class AssessmentAttempt(BaseModel):
    id: str
    user_id: str
    assessment_id: str
    status: AssessmentStatus = AssessmentStatus.NOT_STARTED
    started_at: datetime
    submitted_at: Optional[datetime] = None
    answers: Dict[str, dict] = {} # Question ID to answer payload

class AssessmentResult(BaseModel):
    attempt_id: str
    user_id: str
    assessment_id: str
    overall_score_percent: float
    passed: bool
    competency_scores: Dict[CompetencyArea, float] = {} # Area to percentage score
    strengths: List[CompetencyArea] = []
    weak_areas: List[CompetencyArea] = []
    recommended_lessons: List[str] = []
    retake_recommended: bool = False
    ai_feedback: Optional[str] = None
