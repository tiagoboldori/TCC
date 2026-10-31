
from enum import Enum, auto

class ActivityType (Enum):
    C_START_PROCESSING_SOURCE = auto()
    C_START_PROCESSING_DESTINATION = auto()
    C_START_PROCESSING_GENERIC = auto()
    C_START_TRANSMISSION = auto()