from vertice import Vertice
from aresta import Aresta

class Grafo:
    def __init__(self):
        self.__vertices = []
        self.__arestas = []


    def get_vertices(self) -> list[Vertice]:
        return self.__vertices
    

    def get_vertice(self, id) -> Vertice | None:
        for vertice in self.__vertices:
            if vertice.get_id() == str(id):
                return vertice
        return None
    

    def add_vertice(self,vertice:Vertice) -> None:
        self.__vertices.append(vertice)


    def remove_vertice(self,vertice:Vertice) -> None:
        self.__vertices.remove(vertice)
        for aresta in self.__arestas:
            if vertice in aresta:
                self.__arestas.remove(aresta)


    def get_arestas(self) -> list[Aresta]:
        return self.__arestas
    
    def get_aresta(self, origem:Vertice, destino:Vertice) -> Aresta | None:
        for aresta in self.__arestas:
            if aresta.get_origem() == origem and aresta.get_destino() == destino:
                return aresta
        return None
    
    def add_aresta(self,aresta:Aresta) -> None:
        self.__arestas.append(aresta)


    def remove_aresta(self,aresta:Aresta) -> None:
        self.__arestas.remove(aresta)


    def mostra_grafo(self) -> None:
        print("Vertices:")
        for vertice in self.__vertices:
            print(vertice)
        print("Arestas:")
        for aresta in self.__arestas:
            print(aresta)