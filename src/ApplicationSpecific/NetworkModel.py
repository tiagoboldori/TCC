
from functools import partial
import random

from src.ApplicationSpecific.ActivityType import ActivityType
from src.Engine import TimeCell


class NetworkModel:
    def __init__(self, router, engine):
        
        self.clients = []

        self.router = router
        
        self.engine = engine


    #B's and C's Simulação

    def B_arrival(self, client,  packet_id, activity_type):
        client.add_to_queue(packet_id, activity_type)

    def B_departure(self, client):
        client.set_is_busy(False)
        client.set_current_job(None)




    #Processamento de atividades C
    def C_process_all(self):
        for client in self.clients:
            self.C_process(client)


    def C_process(self, client):

        if not client.is_busy and len(client.get_job_queue()) > 0:
            current_job = client.get_job_queue().popleft()
    
            client.set_current_job(current_job)
    
            packet_id = current_job.get_packet_id()
            activity_type = current_job.get_activity_type()

            client.set_current_job(current_job)
            client.set_is_busy(True)


            match activity_type:
                case ActivityType.C_START_PROCESSING_ASSEMBLY:
                    # valor arbitrario de processamento obtido a partir de uma distribuicao uniforme + tempo da DSA usada * distribuicao uniforme arbitraria de 1.0 até 1.5
                    temp = client.get_packet_list().get_packet(packet_id)
                    packet = temp["packet"]
                    time = temp["time"]
                    processing_time = random.uniform(2,5) + time * random.uniform(1.0, 1.5)

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

                    print(f"Scheduled B_departure for packet {packet_id} at time {self.engine.get_current_time() + processing_time:.2f}.")
                    
                case _:
                    raise ValueError(f"Invalid activity type: {activity_type}")
            