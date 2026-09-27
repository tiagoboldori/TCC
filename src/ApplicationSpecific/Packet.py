
class Packet:
    def __init__(self, data):
        self.__packet_data = data

    def get_data(self):
        return self.__packet_data

    def set_data(self, data):
        self.__packet_data = data