import hashlib
import secrets
import random

from Cliente import Cliente
from Informacao import Info
from Roteador import Roteador

print("Iniciando Teste para BFS")


roteador = Roteador()

print("Criando Clientes aleatórios....")
for i in range(10):
    cliente = Cliente(str(i))

    for cli in roteador.get_all_clientes():
        num = random.randint(1, 2)
        if num == 1:
            cliente.add_adj(cli, Info(1, 1))

    roteador.add_cliente(cliente)
    print(cliente.get_nome(), "Criado!")


clientes = roteador.get_all_clientes()

for c in clientes:
    print(c)


random_num = random.randint(0, len(clientes) - 1)
random_cli_1 = clientes[random_num]
random_num = random.randint(0, len(clientes) - 1)
random_cli_2 = clientes[random_num]


print("Calculando caminho de:", random_cli_1, random_cli_2)

bfs = roteador.bfs(random_cli_1, random_cli_2)

try:
    print("Caminho encontrado:")
    for cli in bfs:
        print(cli.get_nome())
except:
    print("Caminho não encontrado")
