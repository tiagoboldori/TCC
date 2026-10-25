
from src.ApplicationSpecific.ActivityType import ActivityType


class QueueItem:
    def __init__(self, packet_id: int, activity_type: ActivityType):
        self.__activity_type = activity_type
        self.__packet_id = packet_id

    def get_activity_type(self) -> ActivityType:
        return self.__activity_type

    def set_activity_type(self, activity_type: ActivityType):
        self.__activity_type = activity_type


    def get_packet_id(self) -> int:
        return self.__packet_id

    def set_packet_id(self, packet_id):
        self.__packet_id = packet_id