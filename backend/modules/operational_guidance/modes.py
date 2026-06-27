from enum import Enum

class OperationalMode(str, Enum):
    LEARNING = "learning"
    OPERATIONAL = "operational"
    EXPERT = "expert"
