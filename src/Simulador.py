from Roteador import Roteador

class Simulador:
    def __init__(self):
        self.__roteador = Roteador()
        self.__eventos = []


    def get_roteador(self) -> Roteador:
        return self.__roteador

    def set_roteador(self, roteador: Roteador) -> None:
        self.__roteador = roteador


    def get_eventos(self) -> list:
        return self.__eventos

    def set_eventos(self, eventos: list) -> None:
        self.__eventos = eventos
        

    #Eventos
    #Mecanismo de confiabilidade
    