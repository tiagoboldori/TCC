class Evento:
    def __init__(self, origem, destino, inicio, pacote):
        self.__origem = origem
        self.__destino = destino
        self.__tempo_inicio = inicio
        self.__tempo_destino = None
        self.__tempo_fim = None
        self.__pacote = pacote
