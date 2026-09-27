
class NetworkModel:
    def __init__(self, router, engine):
        
        self.clients = []
        self.packets = []

        self.router = router
        
        self.engine = engine


    #B's and C's Simulação

    def B_arrival(self, client,  packet, activity_type):
        client.add_to_queue(packet, activity_type)

    def B_end_job(self, client):
        client.set_current_job(None)
        client.set_next_job(client.get_next_job() + 1)
        client.is_busy = False

    def C_process_all(self):
        for client in self.clients:
            self.C_process(client)

    def C_process(self, client):
        pass