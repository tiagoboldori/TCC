from Roteador import Roteador

class Simulador:
    def __init__(self):
        self.__roteador = Roteador()

    def get_roteador(self) -> Roteador:
        return self.__roteador