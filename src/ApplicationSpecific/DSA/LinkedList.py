from src.ApplicationSpecific.DSA.DSA_Interface import DSA_Interface
from src.ApplicationSpecific.Packet import Packet



class LinkedList(DSA_Interface):
    def __init__(self, head: Node=None):
        self.__head = head




    def get_packet(self, packet_id):
        # Implement the logic to retrieve a packet by its ID
        time=1

        current = self.__head
        

        while current is not None:
            time+=1

            if current.get_id() == packet_id:
                return {"packet":current.get_packet(), "time":time}
            
            current = current.next
        
        return {"packet": None, "time": time}


    def add_packet(self, packet_id, packet):
        # Implement the logic to add a packet by its ID
        new_node = Node(packet_id, packet)
        if self.__head is None:
            self.__head = new_node
        else:
            current = self.__head
            while current.next is not None:
                current = current.next
            current.next = new_node


    def remove_packet(self, packet_id):
        # Implement the logic to remove a packet by its ID
        if self.__head is None:
            return False

        if self.__head.get_id() == packet_id:
            self.__head = self.__head.next
            return True

        current = self.__head

        while current.next is not None:
            if current.next.get_id() == packet_id:
                current.next = current.next.next
                return True
            current = current.next

        return False



class Node:
    def __init__(self, id: int, packet:Packet):
        self.__id = id
        self.__packet = packet
        self.next = None

    def get_id(self):
        return self.__id
    def set_id(self, id):
        self.__id = id


    def get_packet(self):
        return self.__packet
    def set_packet(self, packet):
        self.__packet = packet
