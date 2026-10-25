import random


class Info:
    def __init__(self, latencia: float, perda: float, variancia:float) -> None:
        self.__perda = perda
        # A média não pode ser zero para a Gamma, assumimos um mínimo se necessário
        self.__latencia = max(latencia, 0.001)
        self.__variancia = max(variancia, 0.001)
        
        # Cálculo dos parâmetros da Gamma
        # Média (mu) = alpha * beta
        # Variância (sigma^2) = alpha * beta^2
        self.__beta = self.__variancia / self.__latencia
        self.__alpha = self.__latencia / self.__beta

    def set_latencia(self, latencia: float) -> None:
        self.__latencia = latencia

        

    def get_latencia(self) -> float | None:
        return self.__latencia


    def get_latencia_simulada(self) -> float:
        # random.gammavariate gera o valor estocástico baseado nos botões alpha e beta
        tempo_calculado = random.gammavariate(self.__alpha, self.__beta)
        
        # tempo minimo simulando meio fisico garantindo que a latencia simulada nunca seja menor que 30% da latencia média
        tempo_minimo_fisico = self.__latencia * 0.3 
        return max(tempo_calculado, tempo_minimo_fisico)


    def set_perda(self, perda: float) -> None:
        self.__perda = perda

    def get_perda(self) -> float | None:
        return self.__perda
