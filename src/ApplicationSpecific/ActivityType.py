
from enum import Enum, auto

class ActivityType (Enum):
    C_START_PROCESSING_ASSEMBLY = auto()
    C_START_PROCESSING_DESTINATION = auto()
    C_START_PROCESSING_GENERIC = auto()
    B_END_PROCESSING = auto()
    C_START_TRANSMISSION = auto()
    B_END_TRANSMISSION = auto()