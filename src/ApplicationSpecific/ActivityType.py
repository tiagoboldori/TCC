
from enum import Enum, auto
from collections import deque

class ActivityType (Enum):
    START_PROCESSING = auto()
    END_PROCESSING = auto()
    START_TRANSMISSION = auto()
    END_TRANSMISSION = auto()