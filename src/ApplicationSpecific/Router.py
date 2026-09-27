from src.ApplicationSpecific.Client import Client
from src.ApplicationSpecific.Information import Info


class Router:
    def __init__(self) -> None:
        self.__clientes = []

    # Getter/Setter CLIENTES
    def get_all_clientes(self) -> list[Client]:
        return self.__clientes

    def get_cliente(self, name) -> Client | None:
        for cli in self.get_all_clientes():
            if cli.get_name() == name:
                return cli

    def add_cliente(self, cliente: Client) -> None:
        for c in self.__clientes:
            if c.get_name() == cliente.get_name():
                return

        if cliente not in self.__clientes:
            self.__clientes.append(cliente)


    def add_adj(self, cliente1: Client, cliente2: Client, info:Info) -> None:
        cliente1.add_adj(cliente2, info)
        cliente2.add_adj(cliente1, info)

    #BFS
    def bfs(self, origem: Client, destino: Client) -> list[Client] | None:
        for cli in self.get_all_clientes():
            cli.ant = None

        fila = [origem]
        caminho = []
        visitados = [origem]

        if origem == destino:
            return None

        if len(fila) == 0:
            print("Caminho não encontrado")
            return None

        while len(fila) > 0:
            cli_atual = fila.pop(0)

            if cli_atual == destino:
                while cli_atual.ant != None:
                    caminho.insert(0, cli_atual)
                    cli_atual = cli_atual.ant

                caminho.insert(0, origem)
                return caminho

            for adj in cli_atual.get_all_adj():
                cli_adj = adj[0]
                if cli_adj not in visitados:
                    visitados.append(cli_adj)
                    cli_adj.ant = cli_atual
                    fila.append(cli_adj)

        print("Sem caminho encontrado")
        return
