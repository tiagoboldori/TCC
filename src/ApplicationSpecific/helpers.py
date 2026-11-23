def rtt(netModel):
    
    total = 0
    clients = netModel.get_clients()

    for atual, proximo in zip(clients, clients[1:]):
        adj = atual.get_adj(proximo)
        if adj is None:
            raise ValueError(f"{atual.get_name()} não tem enlace com {proximo.get_name()}")
        total += adj[1].get_latencia()

    return total * 3



# envio apenas de [base, base+ n]
def can_load(client, packet_id: int) -> bool:

    inside_window = packet_id < client.get_current_idx() + client.get_window_size()
    buffer_space = client.get_protocol_buffer().get_size() < client.get_buffer_size()

    return inside_window and buffer_space



def is_acked(client, packet_id: int) -> bool:
    base = client.get_current_idx()

    if packet_id < base:          
        return True
    
    window = client.get_retransmission_window()
    idx = packet_id - base

    return idx < len(window) and window[idx] == 1



#============================================================================
# Estimativa de RTT e timeout adaptativo
# Jacobson/Karels + algoritmo de Karn (RFC 6298; Kurose & Ross, seção 3.5.3)
class RttEstimator:
    ALPHA = 0.125   # peso da nova amostra no EstimatedRTT
    BETA = 0.25     # peso da nova amostra no DevRTT
    K = 4           # margem em desvios

    def __init__(self, initial_timeout: float, max_timeout: float):
        self.__estimated_rtt = None
        self.__dev_rtt = None
        self.__timeout = initial_timeout
        self.__max_timeout = max_timeout
        self.__send_time = {}          # packet_id -> horário do último envio
        self.__retransmitted = set()   # pacotes retransmitidos (Karn)

    def get_timeout(self) -> float:
        return self.__timeout

    def get_estimated_rtt(self):
        return self.__estimated_rtt

    def get_dev_rtt(self):
        return self.__dev_rtt

    def on_send(self, packet_id: int, now: float) -> None:
        if packet_id in self.__send_time:
            self.__retransmitted.add(packet_id)
        self.__send_time[packet_id] = now

    def on_timeout(self) -> None:
    # Karn: sem nenhuma amostra válida, dobra o timeout (até o teto) para conseguir
    # medir o RTT. Depois da primeira amostra o backoff é desligado: no modelo a perda
    # é independente da carga (não há congestionamento), então dobrar só atrasa a recuperação.
        if self.__estimated_rtt is None:
            self.__timeout = min(2 * self.__timeout, self.__max_timeout)

    def on_ack(self, packet_id: int, now: float):
        sent = self.__send_time.pop(packet_id, None)
        was_retransmitted = packet_id in self.__retransmitted
        self.__retransmitted.discard(packet_id)

        # Karn: amostra de pacote retransmitido é ambígua -> descartada
        if sent is None or was_retransmitted:
            return None

        sample = now - sent
        if self.__estimated_rtt is None:          # primeira amostra (RFC 6298, 2.2)
            self.__estimated_rtt = sample
            self.__dev_rtt = sample / 2
        else:                                     # RFC 6298, 2.3: DevRTT antes do EstimatedRTT
            self.__dev_rtt = (1 - self.BETA) * self.__dev_rtt + self.BETA * abs(sample - self.__estimated_rtt)
            self.__estimated_rtt = (1 - self.ALPHA) * self.__estimated_rtt + self.ALPHA * sample

        self.__timeout = min(self.__estimated_rtt + self.K * self.__dev_rtt, self.__max_timeout)
        return sample