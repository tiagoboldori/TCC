class Evento:
    def __init__(self, t_inicio: float, t_fim: float, pacote: str):
        self.__t_inicio = t_inicio
        self.__t_fim = t_fim
        self.__pacote = pacote

    def get_t_inicio(self) -> float:
        return self.__t_inicio

    def get_t_fim(self) -> float:
        return self.__t_fim

    def get_pacote(self) -> str:
        return self.__pacote