from vertice import Vertice

class Aresta:
        def __init__(self,latencia: float | int, perda:float, origem:Vertice, destino:Vertice):
                self.__latencia = latencia
                self.__prob_perda = perda
                self.__adj = [origem, destino]

        def get_latencia(self) -> float | int:
                return self.__latencia

        def set_latencia(self, latencia: float | int):
                self.__latencia = latencia

        def get_prob_perda(self) -> float:
                return self.__prob_perda

        def set_prob_perda(self, perda: float):
                self.__prob_perda = perda

        def get_adj(self):
            return self.__adj

        def set_adj(self,origem, destino):
            return self.__adj

        def __str__(self):
                return f"({self.__adj[0]}, {self.__adj[1]}) | l: {self.__latencia}, p: {self.__prob_perda}"
