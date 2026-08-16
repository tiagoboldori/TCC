class Info:
    def __init__(self, latencia: int, perda: float) -> None:
        self.__latencia = latencia
        self.__perda = perda

    def set_latencia(self, latencia: int) -> None:
        self.__latencia = latencia

    def get_latencia(self) -> int | None:
        return self.__latencia

    def set_perda(self, perda: float) -> None:
        self.__perda = perda

    def get_perda(self) -> float | None:
        return self.__perda
