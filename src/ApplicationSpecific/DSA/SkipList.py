from src.ApplicationSpecific.DSA.DSA_Interface import DSA_Interface
from src.ApplicationSpecific.Packet import Packet

import random


import random

class SkipNode:
    def __init__(self, packet_id, packet, level):
        self.packet_id = packet_id
        self.packet = packet
        self.forward = [None] * (level + 1)

class SkipList(DSA_Interface):
    def __init__(self, max_level=5, p=0.5):
        self.max_level = max_level
        self.p = p
        self.level = 0
        self.size = 0
        self.header = SkipNode(-1, None, max_level)

    def _random_level(self) -> int:
        lvl = 0
        while random.random() < self.p and lvl < self.max_level - 1:
            lvl += 1
        return lvl

    def add_packet(self, packet_id, packet):
        update = [None] * self.max_level
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] is not None and current.forward[i].packet_id < packet_id:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is not None and current.packet_id == packet_id:
            current.packet = packet
            return

        new_level = self._random_level()

        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level

        new_node = SkipNode(packet_id, packet, new_level)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

        self.size += 1

    def get_packet(self, packet_id):
        current = self.header
        time = 1  # Custo base da operação

        # Desce do nível mais alto em uso até o nível 0
        for i in range(self.level, -1, -1):
            while current.forward[i] is not None and current.forward[i].packet_id < packet_id:
                current = current.forward[i]
                time += 1  # Contabiliza cada salto horizontal

        # Avança para o nó candidato no nível 0
        current = current.forward[0]
        time += 1

        if current is not None and current.packet_id == packet_id:
            return {"packet": current.packet, "time": time}

        return {"packet": None, "time": time}

    def remove_packet(self, packet_id):
        update = [None] * self.max_level
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] is not None and current.forward[i].packet_id < packet_id:
                current = current.forward[i]
            update[i] = current

        target = current.forward[0]

        # Se encontrou o pacote, religa os ponteiros pulando o nó removido
        if target is not None and target.packet_id == packet_id:
            for i in range(self.level + 1):
                if update[i].forward[i] != target:
                    break
                update[i].forward[i] = target.forward[i]

            # Reduz o nível atual da SkipList caso os níveis superiores tenham ficado vazios
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1

            self.size -= 1
            return True

        return False

    def get_all_packets(self):
        packets = []
        # Percorre apenas o nível 0, que contém todos os elementos ordenados
        current = self.header.forward[0]
        while current is not None:
            packets.append(current.packet.get_data())
            current = current.forward[0]
        return packets

    def get_size(self):
        return self.size

