from ApplicationSpecific.PacketType import PacketType

class Packet:
    def __init__(self, data: str, packet_type: PacketType = PacketType.DATA):
        self.__data = data
        self.__packet_type = packet_type

    def get_data(self) -> str:
        return self.__data

    def get_packet_type(self) -> PacketType:
        return self.__packet_type

    def set_data(self, data: str) -> None:
        self.__data = data

