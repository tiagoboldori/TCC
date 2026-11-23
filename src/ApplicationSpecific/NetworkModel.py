
from functools import partial
import random

from src.ApplicationSpecific.Client import Client
from src.ApplicationSpecific.helpers import *
from src.ApplicationSpecific.ActivityType import ActivityType
from src.ApplicationSpecific.Information import Info
from src.Engine import TimeCell

    
#PENDENTE: Validar funcionamento geral / testes;
# Implementar NACK e afins
# Implementar calculo de Timeout razoavel
# Pesquisar tempo que um PC demora a realizar a transmissao fisica (disparar o pulso)
        


class NetworkModel:
    def __init__(self, router, engine):

        #route to target
        # clients[0] = source
        # clients[len(clients)-1] = target
        self.clients = []

        self.router = router
        
        self.engine = engine

        self.__total_processing_time = 0.0
        self.__total_lost_packets = 0

    def get_total_processing_time(self):
        return self.__total_processing_time
    def set_total_processing_time(self, total_processing_time):
        self.__total_processing_time = total_processing_time
    
    def get_total_lost_packets(self):
        return self.__total_lost_packets
    def set_total_lost_packets(self, total_lost_packets):
        self.__total_lost_packets = total_lost_packets

    def get_clients(self):
        return self.clients

    

    #Processamento de atividades B
    #Packet ID é o equivalente ao seq_number do pacote
    #Fila de prioridade é criada aqui (transmissao: top; confimação de ACK:mid; etc:low)
    def B_arrival(self, client,  packet_id: int, activity_type: ActivityType):
        client.add_to_queue(packet_id, activity_type)



    def B_departure(self, client: Client):
        client.set_is_busy(False)
        client.set_current_job(None)




    #Processamento de atividades C
    #Assume-se que a chegada de pacotes implica na seguinte sequencia: C_processamento -> C_transmissao
    #Subrotinas a serem simuladas:
    # Janela deslizante respeitando a regra de seq_number (Ver kurose e ross)
    # Timeout para cada pacote nao confirmado dentro da janela 
    # fluxo de ACK e NACK (ver kurose e ross)
    def C_process_all(self):
        for client in self.clients:
            self.C_process(client)


    def C_process(self, client: Client):

        if client.get_is_busy() or not client.has_jobs():
            return

        # LOAD só começa se o pacote estiver dentro da janela e houver espaço no buffer
        def can_start(job):
            if job.get_activity_type() == ActivityType.C_LOAD_PACKET:
                return can_load(client, job.get_packet_id())
            return True

        current_job = client.pop_next_job(can_start)

        if current_job is None:
            print(
                f"[C][ADIADO] Cliente {client.get_name()}: carregamentos aguardam a janela "
                f"ou espaço no buffer ({client.get_protocol_buffer().get_size()}/{client.get_buffer_size()})."
            )
            return
        client.set_current_job(current_job)


        packet_id = current_job.get_packet_id()
        activity_type = current_job.get_activity_type()


        client.set_current_job(current_job)
        client.set_is_busy(True)




        match activity_type:
            case ActivityType.C_START_TRANSMISSION:
                self.C_start_transmission(client, packet_id, activity_type)
            
            case ActivityType.C_START_TRANSMISSION_INVERTED:
                self.C_start_transmission_inverted(client, packet_id, activity_type)

            case ActivityType.C_START_PROCESSING_GENERIC:
                if client == self.clients[0]:
                    self.C_start_processing_source(client, packet_id, activity_type)
                    
                elif client == self.clients[len(self.clients)-1]:
                    self.C_start_processing_destination(client, packet_id, activity_type)
                
                else:
                    self.C_start_processing_generic(client, packet_id, activity_type)
                
            case ActivityType.C_START_PROCESSING_GENERIC_INVERTED:
                if client == self.clients[0]:
                    self.C_start_processing_source(client, packet_id, activity_type)
                    
                elif client == self.clients[len(self.clients)-1]:
                    self.C_start_processing_destination(client, packet_id, activity_type)
                
                else:
                    self.C_start_processing_generic(client, packet_id, activity_type, inverted=True)

            case ActivityType.C_LOAD_PACKET:
                self.C_load_packet(client, packet_id, activity_type)

            case ActivityType.C_PROCESS_ACK:
                self.C_process_ack(client, packet_id)

            case ActivityType.C_PROCESS_NACK:
                self.C_process_nack(client, packet_id)

            case ActivityType.C_PROCESS_TIMEOUT:
                self.C_process_timeout(client, packet_id)
                                    
            case _:
                raise ValueError(f"Invalid activity type: {activity_type}")


    def C_load_packet(self, client: Client, packet_id: int, activity_type: ActivityType):
        #Considera-se apenas pegar um pacote de id:X da memoria da aplicação e duplica-lo para o buffer do protocolo com o mesmo id:X, para que seja transmitido posteriormente
        
        print(
            f"[C][CARREGAMENTO] Cliente {client.get_name()}: iniciando atividade "
            f"{activity_type.name} para pacote #{packet_id}."
        )
        
        packet = client.get_application_memory().get_packet(packet_id)['packet']
        client.get_protocol_buffer().add_packet(packet_id, packet)

        cell = TimeCell(
            name = f"{client.get_name()} B_departure ",
            time = 1,  # Arbitrary processing time for loading packet
            action = partial(
                self.B_departure,
                client
            )
        )
        self.engine.schedule(cell)

        print(f"[B][AGENDADO] {cell.name.strip()} | horário={cell.time:.2f}.")

        client.add_to_queue(packet_id, ActivityType.C_START_PROCESSING_GENERIC)


    #C_START_PROCESSING_SOURCE
    def C_start_processing_source(self, client: Client, packet_id: int, activity_type: ActivityType):
        #Validação de ACK -> Remoção de pacote do buffer respeitando implementações reais do Selective Repeat
        # Validação de ACK / NACK será feita usando IDs Arbitrários de pacotes. -1000 - package_id -> ACK, -2000 - package_id -> NACK
        # Implementar timeout para cada pacote enviado, caso não haja confirmação de recebimento (ACK)


        #POLIR para confirmacao de primeiro pacote da janela
        #Caso ACK (de acordo com nossa convenção de IDs arbitrários)
        if packet_id <= -1000 and packet_id > -2000:
            id = -packet_id - 1000
            window = client.get_retransmission_window()
            window_index = id - client.get_current_idx()
            if not 0 <= window_index < len(window):
                print(
                    f"[C][ACK] Cliente {client.get_name()}: ACK do pacote #{id} "
                    "fora da janela atual; ignorando."
                )
                self.engine.schedule(TimeCell(
                    name=f"{client.get_name()} B_departure",
                    time=0,
                    action=partial(self.B_departure, client),
                ))
                return

            print(
                f"[C][ACK] Cliente {client.get_name()}: ACK do pacote #{id} recebido; "
                "atualizando janela de retransmissão."
            )
            window[window_index] = 1

            client.get_rtt_estimator().on_ack(id, self.engine.get_current_time())

            client.get_protocol_buffer().remove_packet(id)

            while window and window[0] == 1:
                window.pop(0)
                window.append(0)
                client.set_current_idx(client.get_current_idx() + 1)

            cell = TimeCell(
                name = f"{client.get_name()} B_departure",
                time = 0,
                action = partial(
                    self.B_departure,
                    client
                )
            )

            self.engine.schedule(cell)

            return



        # caso NACK package
        elif packet_id <= -2000:
            id = -packet_id - 2000
            window = client.get_retransmission_window()
            window_index = id - client.get_current_idx()
            if not 0 <= window_index < len(window):
                print(
                    f"[C][NACK] Cliente {client.get_name()}: NACK do pacote #{id} "
                    "fora da janela atual; ignorando."
                )
                self.engine.schedule(TimeCell(
                    name=f"{client.get_name()} B_departure for C_process_nack",
                    time=0,
                    action=partial(self.B_departure, client),
                ))
                return

            if window[window_index] == 1:
                print(
                    f"[C][NACK] Cliente {client.get_name()}: pacote #{id} já foi "
                    "confirmado; ignorando NACK duplicado."
                )
                self.engine.schedule(TimeCell(
                    name=f"{client.get_name()} B_departure for C_process_nack",
                    time=0,
                    action=partial(self.B_departure, client),
                ))
                return

            print(
                f"[C][NACK] Cliente {client.get_name()}: NACK do pacote #{id} recebido; "
                "agendando retransmissão."
            )
            window[window_index] = 0

            cell = TimeCell(
                name = f"{client.get_name()} B_departure for C_process_nack",
                time = 0,
                action = partial(
                    self.B_departure,
                    client
                )
            )

            self.engine.schedule(cell)

            #start_transmission routine
            cell = TimeCell(
                name = f"{client.get_name()} B_arrival for C_start_transmission",
                time = 0,
                action = partial(
                    self.B_arrival,
                    client,
                    id,
                    ActivityType.C_START_TRANSMISSION
                )
            )
            print(f"[B][AGENDADO] Retransmissão do pacote #{id} em 0 unidade de tempo.")

            self.engine.schedule(cell)

            return


        #GENERIC PACKAGE
        # PACKAGE != ACK / NACK
        if is_acked(client, packet_id):
            print(
                f"[C][DESCARTE] Cliente {client.get_name()}: pacote #{packet_id} já foi confirmado; retransmissão cancelada"
            )
            self.engine.schedule(TimeCell(
                name=f"{client.get_name()} B_departure",
                time = 0,
                action = partial(self.B_departure, client)
            ))
            return


        temp = client.get_protocol_buffer().get_packet(packet_id)
        packet = temp["packet"]
        time = temp["time"]

        #metrics
        processing_time = random.uniform(2,5) + time * random.uniform(1.0, 1.5)
        self.set_total_processing_time(self.get_total_processing_time() + processing_time)


        print(
            f"[C][PROCESSAMENTO] Cliente {client.get_name()}: pacote #{packet_id}, "
            f"atividade={activity_type.name}, duração={processing_time:.2f}."
        )

        
        cell = TimeCell(
            name = f"{client.get_name()} B_departure for C_start_processing",
            time = processing_time,
            action = partial(
                self.B_departure,
                client
            )
        )

        self.engine.schedule(cell)

            
        print(f"[B][AGENDADO] {cell.name.strip()} | horário={cell.time:.2f}.")

        #start_transmission routine
        cell = TimeCell(
            name = f"{client.get_name()} B_arrival for C_start_transmission",
            time = processing_time,
            action = partial(
                self.B_arrival,
                client,
                packet_id,
                ActivityType.C_START_TRANSMISSION
            )
        )
        print(
            f"[B][AGENDADO] {cell.name.strip()} para o pacote #{packet_id} "
            f"| horário={cell.time:.2f}."
        )
        self.engine.schedule(cell)



    def C_start_processing_destination(self, client: Client, packet_id: int, activity_type: ActivityType):
        processing_time = 0

        #Transmissão de ACK para o source
        cell = TimeCell(
            name = f"{client.get_name()} B_arrival ",
            time = processing_time,  
            action = partial(
                self.B_arrival,
                client,
                (packet_id+1000)*-1,
                ActivityType.C_START_TRANSMISSION_INVERTED
            )
        )
        self.engine.schedule(cell)


        cell = TimeCell(
            name = f"{client.get_name()} B_departure ",
            time = processing_time,
            action = partial(
                self.B_departure,
                client
            )
        )

        self.engine.schedule(cell)
        print(f"[B][AGENDADO] {cell.name.strip()} | horário={cell.time:.2f}.")



    def C_start_processing_generic(self, client: Client, packet_id: int, activity_type: ActivityType, inverted=False):
        
        temp = client.get_protocol_buffer().get_packet(packet_id)
        packet = temp["packet"]
        time = temp["time"]
        processing_time =  time * random.uniform(1.0, 1.5)

        #metrics
        self.set_total_processing_time(self.get_total_processing_time() + processing_time)

        print(
            f"[C][PROCESSAMENTO] Cliente {client.get_name()}: pacote #{packet_id}, "
            f"atividade={activity_type.name}, duração={processing_time:.2f}."
        )

        cell = TimeCell(
            name = f"{client.get_name()} B_departure ",
            time = processing_time,
            action = partial(
                self.B_departure,
                client
            )
        )

        self.engine.schedule(cell)

            
        print(f"[B][AGENDADO] {cell.name.strip()} | horário={cell.time:.2f}.")

        
        if inverted:
            print(
                f"[C][PROCESSAMENTO INVERSO] Pacote #{packet_id} processado por "
                f"{client.get_name()}; retorno ao cliente anterior."
            )
            cell = TimeCell(
                name = f"{client.get_name()} B_arrival ",
                time = processing_time,
                action = partial(
                    self.B_arrival,
                    client,
                    packet_id,
                    ActivityType.C_START_TRANSMISSION_INVERTED
                )
            )

        else:
        #start_transmission routine
            cell = TimeCell(
                name = f"{client.get_name()} B_arrival ",
                time = processing_time,
                action = partial(
                    self.B_arrival,
                    client,
                    packet_id,
                    ActivityType.C_START_TRANSMISSION
                )
            )
        print(
            f"[B][AGENDADO] {cell.name.strip()} para o pacote #{packet_id} "
            f"| horário={cell.time:.2f}."
        )
        self.engine.schedule(cell)


    def C_start_transmission(self, client: Client, packet_id: int, activity_type: ActivityType ):
        if client == self.clients[len(self.clients)-1]:
            print(
                f"[C][TRANSMISSÃO] Cliente {client.get_name()} é o destino; "
                f"não há próximo salto para o pacote #{packet_id}."
            )
            return


        # A FAZER: ADICIONAR TEMPO DE PROCESSAMENTO PARA ATIVIDADE
        print(
            f"[C][TRANSMISSÃO] Cliente {client.get_name()} iniciou o envio do pacote "
            f"#{packet_id} (atividade={activity_type.name}) | horário={self.engine.get_current_time():.2f}."
        )
        #print(f"Scheduling B_departure for packet {packet_id} after transmission time.")

        idx = self.clients.index(client)

        adj = client.get_all_adj()

        if idx < len(self.clients) - 1:
            next_client = self.clients[idx+1]
            for a in adj:
                if a[0] == next_client:
                    info = a[1]
                    break

            # PESQUISAR SOBRE TEMPO DE ENVIO / PROCESSAMENTO PARA ESTE CASO EM ESPECIFICO PARA BASE DE SIMULACAO MELHOR
            # Usando 0 ut para evitar simular NIC e processamento em paralelo como ocorre em cenários reais
            cell = TimeCell(
                name = f"{client.get_name()} B_departure ",
                time = 0,
                action = partial(
                    self.B_departure,
                    client
                )
            )

            self.engine.schedule(cell)    

            print(f"[B][AGENDADO] {cell.name.strip()} | horário={cell.time:.2f}.")



            #AGENDAMENTO DE TIMEOUT
            #pendente correção do tempo de RTT
            packet = client.get_protocol_buffer().get_packet(packet_id)["packet"]
            
            if packet is None:
                print(
                    f"[C][TRANSMISSÃO] Cliente {client.get_name()}: pacote #{packet_id} "
                    "não está no buffer; transmissão cancelada."
                )
                return
            
            if client == self.clients[0]:

                estimator = client.get_rtt_estimator()
                if estimator is None:
                    initial = rtt(self)          # estimativa inicial, antes da 1ª amostra
                    estimator = RttEstimator(initial_timeout=initial, max_timeout=4 * initial)
                    client.set_rtt_estimator(estimator)

                estimator.on_send(packet_id, self.engine.get_current_time())

                cell = TimeCell(
                    name = f"{client.get_name()} B_arrival",
                    time = estimator.get_timeout(),
                    action = partial(
                        self.B_arrival,
                        client,
                        packet_id,
                        ActivityType.C_PROCESS_TIMEOUT
                    )
                )
                self.engine.schedule(cell)
                print(f"[B][TIMEOUT] {cell.name.strip()} | horário={cell.time:.2f}.")

            if info.get_perda() > random.random():
                print(
                    f"[REDE][PERDA] Pacote #{packet_id} perdido no enlace "
                    f"{client.get_name()} -> {next_client.get_name()}."
                )
                self.set_total_lost_packets(self.get_total_lost_packets() + 1)
                return


            activity_type = ActivityType.C_START_PROCESSING_GENERIC

            cell = TimeCell(
                name = f"{next_client.get_name()} B_arrival",
                time = info.get_latencia_simulada(),
                action = partial(
                    self.B_arrival,
                    next_client,
                    packet_id,
                    activity_type
                )
            )

            self.engine.schedule(cell)

            next_client.get_protocol_buffer().add_packet(packet_id, packet)
            
            print(
                f"[B][AGENDADO] {cell.name.strip()} no cliente {next_client.get_name()} "
                f"| horário={cell.time:.2f}."
            )


            


        else:
            print(
                f"[C][TRANSMISSÃO] Cliente {client.get_name()} é a origem; "
                f"não há cliente anterior para o pacote #{packet_id}."
            )
            raise ValueError("No vertex.")
     

    def C_start_transmission_inverted(self, client: Client, packet_id: int, activity_type: ActivityType ):
        if client == self.clients[0]:
            print(
                f"[C][TRANSMISSÃO INVERSA] Cliente {client.get_name()} é a origem; "
                f"não há cliente anterior para o pacote #{packet_id}."
            )
            return


        # A FAZER: ADICIONAR TEMPO DE PROCESSAMENTO PARA ATIVIDADE
        print(
            f"[C][TRANSMISSÃO INVERSA] Cliente {client.get_name()} iniciou o envio do "
            f"pacote #{packet_id} (atividade={activity_type.name}) "
            f"| horário={self.engine.get_current_time():.2f}."
        )

        idx = self.clients.index(client)

        adj = client.get_all_adj()

        if idx <= len(self.clients) - 1 and idx > 0:
            next_client = self.clients[idx-1]
            for a in adj:
                if a[0] == next_client:
                    info = a[1]
                    break



            cell = TimeCell(
                name = f"{client.get_name()} B_departure ",
                time = 0,
                action = partial(
                    self.B_departure,
                    client
                )
            )

            self.engine.schedule(cell)    

            print(f"[B][AGENDADO] {cell.name.strip()} | horário={cell.time:.2f}.")

            if info.get_perda() > random.random():
                print(
                    f"[REDE][PERDA] Pacote #{packet_id} perdido no enlace inverso "
                    f"{client.get_name()} -> {next_client.get_name()}."
                )
                self.set_total_lost_packets(self.get_total_lost_packets() + 1)
                return


            activity_type = ActivityType.C_START_PROCESSING_GENERIC_INVERTED

            cell = TimeCell(
                name = f"{next_client.get_name()} B_arrival",
                time = info.get_latencia_simulada(),
                action = partial(
                    self.B_arrival,
                    next_client,
                    packet_id,
                    activity_type
                )
            )

            self.engine.schedule(cell)

            if packet_id >= 0:
                next_client.get_protocol_buffer().add_packet(
                    packet_id,
                    client.get_protocol_buffer().get_packet(packet_id)["packet"]
                )
            
            print(
                f"[B][AGENDADO] {cell.name.strip()} no cliente {next_client.get_name()} "
                f"| horário={cell.time:.2f}."
            )


        else:
            print(
                f"[C][TRANSMISSÃO INVERSA] Cliente {client.get_name()} é a origem; "
                f"não há cliente anterior para o pacote #{packet_id}."
            )
            raise ValueError("No vertex.")
        


    def C_process_ack(self, client: Client, packet_id: int):
        print(
            f"[C][ACK] Cliente {client.get_name()}: confirmação do pacote #{packet_id} "
            "recebida; removendo do buffer de protocolo."
        )
        client.get_protocol_buffer().remove_packet(packet_id)

        cell = TimeCell(
            name = f"{client.get_name()} B_departure for C_process_ack",
            time = 0,
            action = partial(
                self.B_departure,
                client
            )
        )

        self.engine.schedule(cell)   


    def C_process_nack(self, client: Client, packet_id: int):
        print(
            f"[C][NACK] Cliente {client.get_name()}: solicitação de retransmissão "
            f"recebida para o pacote #{packet_id}."
        )
        # Logic to retransmit the packet can be added here

        cell = TimeCell(
            name = f"{client.get_name()} B_departure for C_process_nack",
            time = 0,
            action = partial(
                self.B_departure,
                client
            )
        )

        self.engine.schedule(cell)


    
    def C_process_timeout(self, client: Client, packet_id: int):
        print(
            f"[C][TIMEOUT] Cliente {client.get_name()}: expirou o tempo de confirmação "
            f"do pacote #{packet_id}."
        )
        # Logic to retransmit the packet can be added here
        window = client.get_retransmission_window()
        window_index = packet_id - client.get_current_idx()
        if not 0 <= window_index < len(window):
            print(
                f"[C][TIMEOUT] Pacote #{packet_id} já não pertence à janela atual; "
                "retransmissão ignorada."
            )

        elif window[window_index] == 1:
            print(
                f"[C][TIMEOUT] Pacote #{packet_id} já foi confirmado; "
                "retransmissão desnecessária."
            )

        
        else:
            client.get_rtt_estimator().on_timeout()
            cell = TimeCell(
                name = f"{client.get_name()} B_arrival",
                time = 0.1,
                action = partial(
                    self.B_arrival,
                    client,
                    packet_id,
                    ActivityType.C_START_PROCESSING_GENERIC
                )
            )
            self.engine.schedule(cell)
            print(
                f"[B][AGENDADO] Retransmissão do pacote #{packet_id} "
                f"| horário={cell.time:.2f}."
            )
        
        cell = TimeCell(
            name = f"{client.get_name()} B_departure",
            time = 0,
            action = partial(
                self.B_departure,
                client
            )
        )

        self.engine.schedule(cell)
        print(f"[B][AGENDADO] {cell.name.strip()} | horário={cell.time:.2f}.")
