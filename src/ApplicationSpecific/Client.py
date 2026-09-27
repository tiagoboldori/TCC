from collections import deque

from src.ApplicationSpecific.QueueItem import QueueItem


# Nome é identificador de cliente
# Representação por lista de adjacencias.
# adj = [[Cliente, Info], [Cliente2, Info2], ...]





class Client:
    def __init__(self, name: str) -> None:

        self.__name = name
        self.__adj = []
        self.is_busy = False

        self.__queue = deque()
        self.__current_job = None
        self.__next_job = 0



    #Setters e Getters para fila de pacotes
    def get_queue(self):
        return self.__queue
    def set_queue(self, queue):
        self.__queue = queue

    def add_to_queue(self, packet, activity_type):
        self.__queue.append(QueueItem(packet, activity_type))

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

    def add_adj(self, client, info) -> None:
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
