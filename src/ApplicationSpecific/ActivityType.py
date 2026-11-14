
from enum import Enum, auto

class ActivityType (Enum):
    C_LOAD_PACKET = auto()
    C_START_PROCESSING_SOURCE = auto()
    C_START_PROCESSING_DESTINATION = auto()
    C_START_PROCESSING_GENERIC = auto()
    C_START_PROCESSING_GENERIC_INVERTED = auto()
    C_START_TRANSMISSION = auto()
    C_START_TRANSMISSION_INVERTED = auto()
    C_PROCESS_TIMEOUT = auto()
    C_PROCESS_NACK = auto()
    C_PROCESS_ACK = auto()