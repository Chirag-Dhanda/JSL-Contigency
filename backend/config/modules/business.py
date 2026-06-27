from .base import AppBaseSettings

class LearningSettings(AppBaseSettings):
    enable_assessments: bool = True
    
    model_config = {"env_prefix": "LEARN_"}

class AnalyticsSettings(AppBaseSettings):
    enable_telemetry: bool = False
    
    model_config = {"env_prefix": "ANALYTICS_"}
