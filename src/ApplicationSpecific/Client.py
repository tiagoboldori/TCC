from collections import deque

from src.ApplicationSpecific.Information import Info
from src.ApplicationSpecific.QueueItem import QueueItem
from src.ApplicationSpecific.config import config_loader


# Nome é identificador de cliente
# Representação por lista de adjacencias.
# adj = [[Cliente, Info], [Cliente2, Info2], ...]




class Client:
    def __init__(self, name: str, data_structure: str) -> None:

        self.__name = name
        self.__adj = []
        self.is_busy = False

        self.__job_queue = deque()
        self.__current_job = None
        self.__next_job = 0


        self.__packet_list = config_loader.DSAs[data_structure]()



    #Setters e Getters para fila de pacotes
    def get_job_queue(self):
        return self.__job_queue
    
    def set_job_queue(self, queue):
        self.__job_queue = queue


    def add_to_queue(self, packet_id, activity_type):
        self.__job_queue.append(QueueItem(packet_id, activity_type))

    def remove_from_queue(self, queueItem):
        for item in self.__job_queue:
            if item == queueItem:
                self.__job_queue.remove(item)
                return


    # GETTER PARA LISTA DE PACOTES (dsa)
    def get_packet_list(self):
        return self.__packet_list



    #getter e setter is_busy
    def get_is_busy(self):
        return self.is_busy

    def set_is_busy(self, busy):
        self.is_busy = busy

    #Setters e Getters para pacote atual
    def get_current_job(self):
        return self.__current_job

    def set_current_job(self, job):
        self.__current_job = job

    #Setters e Getters para próximo pacote
    def get_next_job(self):
        return self.__next_job

    def set_next_job(self, job):
        self.__next_job = job





    # Setter e Getter NOME
    def set_name(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str | None:
        return self.__name


    # Setter e Getter ADJACENCIAS
    def set_adj(self, adj: list) -> None:
        self.__adj = adj

    def add_adj(self, client: Client, info: Info) -> None:
        for i in self.get_all_adj():
            if i[0] == client:
                return

        self.__adj.append([client, info])

    def get_adj(self, client):
        for adj in self.get_all_adj():
            if adj[0] == client:
                return adj
            
    def get_all_adj(self) -> list:
        return self.__adj


            

    # PRINT
    def __str__(self) -> str:
        texto = "\n______ \nCLIENTE " + str(self.get_name()) + "\n Adjacencias:"
        for adj in self.get_all_adj():
            texto += "\n" + str(self.get_name()) + " --> " + adj[0].get_name()

        return texto
