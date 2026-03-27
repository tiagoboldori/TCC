import Vertice

class Roteador:
    def __init__(self, trajeto:list[Vertice], pacotes):
        self.__trajeto = trajeto
        self.__atual = 0
        self.__hora_inicio = None
        self.__pacote_atual = 0
        self.__pacotes = pacotes
