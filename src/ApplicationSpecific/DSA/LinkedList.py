from src.ApplicationSpecific.DSA.DSA_Interface import DSA_Interface
from src.ApplicationSpecific.Packet import Packet



class LinkedList(DSA_Interface):
    def __init__(self, head: Node=None):
        self.__head = head
        self.__size = 0




    def get_packet(self, packet_id) -> dict:
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
        # insere no fim; se o id já existe, só atualiza o pacote (mesmo comportamento da SkipList)
        if self.__head is None:
            self.__head = Node(packet_id, packet)
            self.__size += 1
            return

        current = self.__head
        while True:
            if current.get_id() == packet_id:
                current.set_packet(packet)
                return
            if current.next is None:
                break
            current = current.next

        current.next = Node(packet_id, packet)
        self.__size += 1


    def remove_packet(self, packet_id):
        # o tamanho só diminui se o pacote foi de fato removido
        if self.__head is None:
            return False

        if self.__head.get_id() == packet_id:
            self.__head = self.__head.next
            self.__size -= 1
            return True

        current = self.__head
        while current.next is not None:
            if current.next.get_id() == packet_id:
                current.next = current.next.next
                self.__size -= 1
                return True
            current = current.next

        return False
    
    def get_all_packets(self):
        return []

    def get_size(self):
        return self.__size


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



    
