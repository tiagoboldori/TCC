
from functools import partial
import random

from src.ApplicationSpecific.Client import Client
from src.ApplicationSpecific.ActivityType import ActivityType
from src.ApplicationSpecific.Information import Info
from src.Engine import TimeCell


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

    #Processamento de atividades B
    #Packet ID é o equivalente ao seq_number do pacote
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
        #ADICIONAR VERIFICACAO POR PACOTES DISPONIVEIS NA APLICAÇÃO (verificar se há espaço no buffer de memória do selective repeat)
        for client in self.clients:
            self.C_process(client)


    def C_process(self, client: Client):

        if not client.get_is_busy() and len(client.get_job_queue()) > 0:


            # VALIDAÇÂO PARA PACKET_LOAD
            # Packet load deve respeitar tamanho do buffer do protocolo
            # Caso não haja espaço, busca o proximo evento tipo C que não seja do tipo LOAD_PACKET
            # Falta: implementar evento do load packet, trocar referencias antigas (packet_list) para o buffer do protocolo (protocol_buffer)
            # trocar implementação atual para que processamentos busquem do buffer do protocolo na origem e no destino
            # fazer com que processamento de atividade C load packet busque do application memory e insira diretamente no protocol buffer
            
            # no mais: durante transmissao deve ser gerado evento B para timeout individual do pacote
            # durante processamento de pacote ACK deve-se remover o timeout do pacote enviado
            # ao receber pacote NACK deve-se remanejar timeout agendado
            if client.get_job_queue()[0].get_activity_type() == ActivityType.C_LOAD_PACKET and client.get_protocol_buffer().get_size() >= client.get_buffer_size():
                    
                    keep = client.get_job_queue()

                    while client.get_job_queue():
                            current_job = client.get_job_queue().popleft()
                            if current_job.get_activity_type() != ActivityType.C_LOAD_PACKET:
                                break
                            else:
                                keep.append(current_job)

                    client.set_job_queue(keep)

            else:

                current_job = client.get_job_queue().popleft()
                    
            client.set_current_job(current_job)
    
            packet_id = current_job.get_packet_id()
            activity_type = current_job.get_activity_type()

            client.set_current_job(current_job)
            client.set_is_busy(True)


            match activity_type:
                case ActivityType.C_START_TRANSMISSION:
                    self.C_start_transmission(client, packet_id, activity_type)

                case ActivityType.C_START_PROCESSING_GENERIC:
                    # valor arbitrario de processamento obtido a partir de uma distribuicao uniforme + tempo da DSA usada * distribuicao uniforme arbitraria de 1.0 até 1.5 (para source / destination)
                    if client == self.clients[0]:
                        self.C_start_processing_source(client, packet_id, activity_type)
                        
                    elif client == self.clients[len(self.clients)-1]:
                        self.C_start_processing_destination(client, packet_id, activity_type)
                    
                    else:
                        self.C_start_processing_generic(client, packet_id, activity_type)
                    
                case ActivityType.C_LOAD_PACKET:
                    self.C_load_packet(client, packet_id, activity_type)
                                        
                case _:
                    raise ValueError(f"Invalid activity type: {activity_type}")


    def C_load_packet(self, client: Client, packet_id: int, activity_type: ActivityType):
        #Considera-se apenas pegar um pacote de id:X da memoria da aplicação e duplica-lo para o buffer do protocolo com o mesmo id:X, para que seja transmitido posteriormente
        
        print(f"Starting Activity {activity_type}\nLoading packet {packet_id} from application memory to protocol buffer...")
        
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

        print(f"Scheduled B_departure for activity {cell.name} at time {self.engine.get_current_time() + 1:.2f}.")

        client.add_to_queue(packet_id, ActivityType.C_START_PROCESSING_GENERIC)


    #C_START_PROCESSING_SOURCE
    def C_start_processing_source(self, client: Client, packet_id: int, activity_type: ActivityType):
        #Validação de ACK -> Remoção de pacote do buffer respeitando implementações reais do Selective Repeat
        # ....
        # if packet.get_packet_type() == PacketType.ACK:
        #     print(f"Packet {packet_id} is an ACK. Removing from buffer.")
        #     return

        temp = client.get_protocol_buffer().get_packet(packet_id)
        packet = temp["packet"]
        time = temp["time"]

        #metrics
        processing_time = random.uniform(2,5) + time * random.uniform(1.0, 1.5)
        self.set_total_processing_time(self.get_total_processing_time() + processing_time)



        print(f"Client {client.get_name()} is processing packet {packet_id} with activity type {activity_type} for {processing_time:.2f} time units.")

        
        cell = TimeCell(
            name = f"{client.get_name()} B_departure ",
            time = processing_time,
            action = partial(
                self.B_departure,
                client
            )
        )

        self.engine.schedule(cell)

            
        print(f"Scheduled B_departure for activity {cell.name} at time {self.engine.get_current_time() + processing_time:.2f}.")
        print(f"")

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
        print(f"Scheduling B_arrival for packet {packet_id} after processing time.")
        self.engine.schedule(cell)



    def C_start_processing_destination(self, client: Client, packet_id: int, activity_type: ActivityType):

        cell = TimeCell(
            name = f"{client.get_name()} B_departure ",
            time = 1,  # Arbitrary processing time for destination processing
            action = partial(
                self.B_departure,
                client
            )
        )

        self.engine.schedule(cell)



    def C_start_processing_generic(self, client: Client, packet_id: int, activity_type: ActivityType):
        # Implement the logic for processing a generic packet
        temp = client.get_protocol_buffer().get_packet(packet_id)
        packet = temp["packet"]
        time = temp["time"]
        processing_time = random.uniform(1,3) + time * random.uniform(1.0, 1.5)

        #metrics
        self.set_total_processing_time(self.get_total_processing_time() + processing_time)

        print(f"Client {client.get_name()} is processing packet {packet_id} with activity type {activity_type} for {processing_time:.2f} time units.")

        
        cell = TimeCell(
            name = f"{client.get_name()} B_departure ",
            time = processing_time,
            action = partial(
                self.B_departure,
                client
            )
        )

        self.engine.schedule(cell)

            
        print(f"Scheduled B_departure for activity {cell.name} at time {self.engine.get_current_time() + processing_time:.2f}.")
        print(f"")

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
        print(f"Scheduling B_arrival for packet {packet_id} after processing time.")
        self.engine.schedule(cell)


    def C_start_transmission(self, client: Client, packet_id: int, activity_type: ActivityType):

        #implementar janela deslizante confimação (ACK e NACK)
        if client == self.clients[len(self.clients)-1]:
            print(f"Client {client.get_name()} is the last client in the network. No next client to transmit to.")
            return


        # A FAZER: ADICIONAR TEMPO DE PROCESSAMENTO PARA ATIVIDADE
        print(f"Client {client.get_name()} is starting transmission for packet {packet_id} with activity type {activity_type} at time {self.engine.get_current_time():.2f}.")
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
            # Atualmente agendado para 1 ut no futuro de forma arbitraria.
            cell = TimeCell(
                name = f"{client.get_name()} B_departure ",
                time = 1,
                action = partial(
                    self.B_departure,
                    client
                )
            )

            self.engine.schedule(cell)    

            if info.get_perda() > random.random():
                print(f"Packet {packet_id} lost during transmission from {client.get_name()} to {next_client.get_name()}.")
                self.set_total_lost_packets(self.get_total_lost_packets() + 1)
                return
            
            

            
                
            print(f"Scheduled B_departure for current Transmission Activity {cell.name} at time {self.engine.get_current_time()+2} ")
            print(f"")


            activity_type = ActivityType.C_START_PROCESSING_GENERIC

            cell = TimeCell(
                name = f"{next_client.get_name()} B_arrival ",
                time = info.get_latencia_simulada(),
                action = partial(
                    self.B_arrival,
                    next_client,
                    packet_id,
                    activity_type
                )
            )

            self.engine.schedule(cell)

            next_client.get_protocol_buffer().add_packet(packet_id, client.get_protocol_buffer().get_packet(packet_id)["packet"])
            
            print(f"Scheduled B_arrival for activity {cell.name} at time {self.engine.get_current_time() + info.get_latencia_simulada():.2f}. at client {next_client.get_name()}.")



        else:
            #adicionar B_departure para caso abaixo
            print(f"Client {client.get_name()} is the last client in the network. No next client to transmit to.")
            raise ValueError("No vertex.")
        