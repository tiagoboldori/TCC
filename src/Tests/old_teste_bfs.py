import random

from Cliente import Cliente
from Informacao import Info
from Roteador import Roteador



#provisorio
from src.SimulationEngine import Simulador


print("=" * 50)
print(" TESTE ALEATÓRIO DE BUSCA EM LARGURA (BFS) ".center(50))
print("=" * 50)

roteador = Roteador()

# -------------------------
# Criação dos clientes
# -------------------------

NUM_CLIENTES = 10

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

        # 20% de chance de criar a aresta
        if random.random() < 0.20:
            roteador.add_adj(origem, destino, Info(1, 1))

# -------------------------
# Mostrar o grafo
# -------------------------

print("\n[TESTE][GRAFO] Topologia gerada:\n")

for cliente in clientes:
    print(f"  {cliente.get_nome()} -> ", end="")

    adjs = cliente.get_all_adj()

    if len(adjs) == 0:
        print("(sem conexões)")
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
print(f"[TESTE][ROTA] Origem:  {origem.get_nome()}")
print(f"[TESTE][ROTA] Destino: {destino.get_nome()}")
print("=" * 50)

# -------------------------
# Executa BFS
# -------------------------

caminho = roteador.bfs(origem, destino)

# -------------------------
# Resultado
# -------------------------

if caminho is None:
    print("\n[TESTE][RESULTADO] Nenhum caminho foi encontrado.")
else:
    print("\n[TESTE][RESULTADO] Caminho encontrado:")

    print("  " + " -> ".join(cli.get_nome() for cli in caminho))




sim = Simulador()

sim.set_roteador(roteador)

sim.start()