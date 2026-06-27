from typing import Dict, Optional
from logging import getLogger
from .models import LessonWorkspace, LearnerTools

logger = getLogger("LessonService")

class LessonService:
    def __init__(self):
        self._workspaces: Dict[str, LessonWorkspace] = {}
        self._learner_tools: Dict[str, LearnerTools] = {} # Keyed by user_id:lesson_id

    def load_workspace(self, lesson_id: str) -> Optional[LessonWorkspace]:
        """Loads a prepared Lesson Workspace with all its content blocks."""
        logger.info(f"Loading Workspace for Lesson: {lesson_id}")
        return self._workspaces.get(lesson_id)

    def initialize_workspace(self, workspace: LessonWorkspace):
        """Mock method to populate the service with a workspace."""
        self._workspaces[workspace.lesson_id] = workspace

    def get_learner_tools(self, user_id: str, lesson_id: str) -> LearnerTools:
        """Retrieves or initializes learner tools (state) for a specific lesson."""
        key = f"{user_id}:{lesson_id}"
        if key not in self._learner_tools:
            self._learner_tools[key] = LearnerTools(user_id=user_id, lesson_id=lesson_id)
            logger.info(f"Initialized new LearnerTools for User: {user_id}, Lesson: {lesson_id}")
        return self._learner_tools[key]

    def add_bookmark(self, user_id: str, lesson_id: str, block_id: str) -> LearnerTools:
        """Adds a bookmark to a specific block in the lesson."""
        tools = self.get_learner_tools(user_id, lesson_id)
        if block_id not in tools.bookmarks:
            tools.bookmarks.append(block_id)
            logger.debug(f"Added bookmark for block {block_id}")
        return tools

    def save_personal_note(self, user_id: str, lesson_id: str, block_id: str, note: str) -> LearnerTools:
        """Saves a personal note attached to a specific block."""
        tools = self.get_learner_tools(user_id, lesson_id)
        tools.personal_notes[block_id] = note
        logger.debug(f"Saved personal note for block {block_id}")
        return tools

    def update_progress(self, user_id: str, lesson_id: str, percent: float) -> LearnerTools:
        """Updates the learner's reading/scroll progress in the lesson."""
        tools = self.get_learner_tools(user_id, lesson_id)
        tools.reading_progress_percent = max(0.0, min(100.0, percent))
        logger.debug(f"Updated progress to {percent}% for lesson {lesson_id}")
        return tools
