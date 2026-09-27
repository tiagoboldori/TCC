
class QueueItem:
    def __init__(self, packet, activity_type):
        self.__activity_type = activity_type
        self.__packet = packet

    def get_activity_type(self):
        return self.__activity_type

    def set_activity_type(self, activity_type):
        self.__activity_type = activity_type


    def get_packet(self):
        return self.__packet

    def set_packet(self, packet):
        self.__packet = packet