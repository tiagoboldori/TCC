import random

from Cliente import Cliente
from Informacao import Info
from Roteador import Roteador

print("=" * 50)
print("TESTE ALEATÓRIO - BFS")
print("=" * 50)

roteador = Roteador()

# -------------------------
# Criação dos clientes
# -------------------------

NUM_CLIENTES = 20

for i in range(NUM_CLIENTES):
    roteador.add_cliente(Cliente(str(i)))

clientes = roteador.get_all_clientes()

# -------------------------
# Criação das arestas
# -------------------------

for origem in clientes:
    for destino in clientes:
        # Não cria laço para ele mesmo
        if origem == destino:
            continue

        # 30% de chance de criar a aresta
        if random.random() < 0.20:
            origem.add_adj(destino, Info(1, 1))

# -------------------------
# Mostrar o grafo
# -------------------------

print("\nGRAFO GERADO\n")

for cliente in clientes:
    print(f"{cliente.get_nome()} -> ", end="")

    adjs = cliente.get_all_adj()

    if len(adjs) == 0:
        print("[]")
        continue

    print(", ".join(adj[0].get_nome() for adj in adjs))

# -------------------------
# Escolhe origem e destino
# -------------------------

origem = random.choice(clientes)
destino = random.choice(clientes)

while origem == destino:
    destino = random.choice(clientes)

print("\n" + "=" * 50)
print(f"Origem : {origem.get_nome()}")
print(f"Destino: {destino.get_nome()}")
print("=" * 50)

# -------------------------
# Executa BFS
# -------------------------

caminho = roteador.bfs(origem, destino)

# -------------------------
# Resultado
# -------------------------

if caminho is None:
    print("\nNenhum caminho encontrado.")
else:
    print("\nCaminho encontrado:")

    print(" -> ".join(cli.get_nome() for cli in caminho))
