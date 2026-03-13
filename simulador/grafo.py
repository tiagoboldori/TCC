class Grafo:
    def __init__(self):
        self.vertices = []
        self.arestas = []
    
    def adicionar_vertice(self, vertice):
        self.vertices.append(vertice)
    
    def adicionar_aresta(self, aresta):
        self.arestas.append(aresta)