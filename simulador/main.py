from vertice import Vertice
from aresta import Aresta
from grafo import Grafo

grafo  = Grafo()

print(" -> 1 para adicionar vertice \n -> 2 para adicionar aresta \n -> 3 para mostrar grafo \n -> 4 para remover vertice \n -> 5 para remover aresta \n -> 0 para sair")
entrada = input()
while entrada!="0":
    print("")
    match entrada:
        case "1":
            id = input("Digite o id do vertice: ")
            grafo.add_vertice(Vertice(id))
        case "2":
            latencia = float(input("Digite a latencia da aresta: "))
            perda = float(input("Digite a probabilidade de perda da aresta: "))
            origem = input("Digite o id do vertice de origem: ")
            destino = input("Digite o id do vertice de destino: ")
            grafo.add_aresta(Aresta(latencia, perda, grafo.get_vertice(origem), grafo.get_vertice(destino)))
        case "3":
            grafo.mostra_grafo()
        case "4":
            id = input("Digite o id do vertice a ser removido: ")
            grafo.remove_vertice(grafo.get_vertice(id))
        case "5":
            origem = input("Digite o id do vertice de origem da aresta a ser removida: ")
            destino = input("Digite o id do vertice de destino da aresta a ser removida: ")
            o = grafo.get_vertice(int(origem))
            d = grafo.get_vertice(int(destino))
            grafo.remove_aresta2(o,d)
            print("==============================================================================")
    entrada = input(" -> 1 para adicionar vertice \n -> 2 para adicionar aresta \n -> 3 para mostrar grafo \n -> 4 para remover vertice \n -> 5 para remover aresta \n -> 0 para sair")
