from vertice import Vertice

class Aresta:
        def __init__(self,latencia: float | int, perda:float, origem:Vertice, destino:Vertice):
                self.__latencia = latencia
                self.__prob_perda = perda
                self.__origem = origem
                self.__destino = destino

        def get_latencia(self) -> float | int:
                return self.__latencia
        
        def set_latencia(self, latencia: float | int):
                self.__latencia = latencia

        def get_prob_perda(self) -> float:
                return self.__prob_perda
        
        def set_prob_perda(self, perda: float):
                self.__prob_perda = perda

        def get_origem(self) -> Vertice:
                return self.__origem
        
        def set_origem(self, origem: Vertice):
                self.__origem = origem

        
        def get_destino(self) -> Vertice:
                return self.__destino
        
        def set_destino(self, destino: Vertice):
                self.__destino = destino

        def __str__(self):
                return f"({self.__origem}, {self.__destino}) | l: {self.__latencia}, p: {self.__prob_perda}"