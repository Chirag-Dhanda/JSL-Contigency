from typing import Dict
from .models import LearningMaterial, LearningExperience
from exceptions.base import NotFoundException
from logging import getLogger

logger = getLogger("LearningService")

class LearningService:
    def __init__(self):
        self._materials: Dict[str, LearningMaterial] = {}
        self._experiences: Dict[str, LearningExperience] = {}
        
    def register_material(self, material: LearningMaterial):
        self._materials[material.id] = material
        
    def get_material(self, material_id: str) -> LearningMaterial:
        if material_id not in self._materials:
            raise NotFoundException(f"Learning Material {material_id} not found.")
        return self._materials[material_id]

    def create_learning_experience(self, experience: LearningExperience) -> LearningExperience:
        self._experiences[experience.id] = experience
        logger.info(f"Created Learning Experience for Knowledge Object: {experience.knowledge_object_id}")
        return experience

    def get_learning_experience(self, experience_id: str) -> LearningExperience:
        if experience_id not in self._experiences:
            raise NotFoundException(f"Learning Experience {experience_id} not found.")
        return self._experiences[experience_id]
