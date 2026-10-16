from src.ApplicationSpecific.DSA.DSA_Interface import DSA_Interface
from src.ApplicationSpecific.Packet import Packet


class SkipList(DSA_Interface):
    def __init__(self , max_level = 5, p = 0.5):
        self.max_level = max_level
        self.p = p
        #self.header = self.create_node(self.max_level, None, None)
        self.items = [[] for _ in range(max_level)]



    def get_packet(self, packet_id):
        # Implement the logic to retrieve a packet by its ID
        i = self.max_level - 1
        time = 1

        while i >= 0:
            for item in self.items[i]:
                time += 1
                if item[0] == packet_id:
                    return {"packet": item[1], "time": time}
            i -= 1

        return {"packet": None, "time": time}



    def add_packet(self, packet_id, packet):
        for i in range(self.max_level):
            if len(self.items[i]) == 0 or self.items[i][-1][0] < packet_id:
                self.items[i].append((packet_id, packet))
                break
            else:
                for j in range(len(self.items[i])):
                    if self.items[i][j][0] == packet_id:
                        self.items[i][j] = (packet_id, packet)
                        return
                    elif self.items[i][j][0] > packet_id:
                        self.items[i].insert(j, (packet_id, packet))
                        return 
        return 
    

    def remove_packet(self, packet_id):
        # Implement the logic to remove a packet by its ID
        pass


