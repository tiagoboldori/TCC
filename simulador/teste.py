from Cliente import Cliente
from Informacao import Info
from Roteador import Roteador

roteador = Roteador()
cli1 = Cliente("cli1")
cli2 = Cliente("cli2")
cli3 = Cliente("cli3")

cli1.add_adj(cli2, Info(1, 1))
cli2.add_adj(cli3, Info(1, 1))

roteador.add_cliente(cli1)
roteador.add_cliente(cli2)
roteador.add_cliente(cli3)

bfs = roteador.bfs(cli1, cli3)

for cli in bfs:
    print(cli.get_nome())
