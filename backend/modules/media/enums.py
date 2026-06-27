from enum import Enum

class MediaType(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    DOCUMENT = "DOCUMENT"
    AUDIO = "AUDIO"
    ANIMATION = "ANIMATION"
    ICON = "ICON"
    MODEL_3D = "MODEL_3D"
    AR_ASSET = "AR_ASSET"
