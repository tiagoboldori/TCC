
from enum import Enum, auto

class PacketType (Enum):
    DATA = auto()
    ACK = auto()
    NACK = auto()