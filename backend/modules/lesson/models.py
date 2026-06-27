from typing import List, Optional, Annotated
from pydantic import BaseModel, Field
from backend.modules.content.models import ContentBlock

class LessonNavigation(BaseModel):
    previous_lesson_id: Optional[str] = None
    next_lesson_id: Optional[str] = None
    table_of_contents: List[str] = []
    breadcrumbs: List[str] = []

class LearnerTools(BaseModel):
    user_id: str
    lesson_id: str
    bookmarks: List[str] = [] # list of block ids
    personal_notes: dict = {} # dict mapping block_id to string
    highlights: dict = {} # dict mapping block_id to highlighted text
    is_favourite: bool = False
    reading_progress_percent: float = 0.0
    estimated_time_remaining_mins: int = 0
    theme: str = "LIGHT"
    font_size: str = "MEDIUM"
    accessibility_mode: bool = False

class LessonFooter(BaseModel):
    summary: str
    objectives_achieved: List[str] = []
    related_lessons: List[str] = []
    recommended_next_lesson_id: Optional[str] = None
    upcoming_assessment_id: Optional[str] = None

class LessonWorkspace(BaseModel):
    lesson_id: str
    title: str
    navigation: LessonNavigation
    blocks: List[Annotated[ContentBlock, Field(discriminator="type")]]
    footer: LessonFooter
