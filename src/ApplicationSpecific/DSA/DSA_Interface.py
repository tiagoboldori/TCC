from abc import ABC, abstractmethod

class DSA_Interface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_packet(self, packet_id) -> dict:
        # Implement the logic to retrieve a packet by its ID
        pass

    @abstractmethod
    def add_packet(self, packet_id, packet):
        # Implement the logic to add a packet by its ID
        pass

    @abstractmethod
    def remove_packet(self, packet_id):
        # Implement the logic to remove a packet by its ID
        pass



