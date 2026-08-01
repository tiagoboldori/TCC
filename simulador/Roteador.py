from Cliente import Cliente


class Roteador:
    def __init__(self) -> None:
        self.__clientes = []

    # Getter/Setter CLIENTES
    def get_all_clientes(self) -> list[Cliente]:
        return self.__clientes

    def get_cliente(self, nome) -> Cliente | None:
        for cli in self.get_all_clientes():
            if cli.get_nome() == nome:
                return cli

    def add_cliente(self, cliente: Cliente) -> None:
        for c in self.__clientes:
            if c.get_nome() == cliente.get_nome():
                return

        if cliente not in self.__clientes:
            self.__clientes.append(cliente)

    # Métodos de Busca BFS
    def bfs(self, origem: Cliente, destino: Cliente) -> list[Cliente] | None:

        fila = [adj[0] for adj in origem.get_all_adj()]
        caminho = []

        if origem == destino:
            return None

        if len(fila) == 0:
            print("Caminho não encontrado")
            return None

        for cli in fila:
            cli.ant = origem

        while len(fila) > 0:
            cli_atual = fila.pop(0)
            for adj in cli_atual.get_all_adj():
                cli_adj = adj[0]
                cli_adj.ant = cli_atual
                fila.append(cli_adj)

            if cli_atual == destino:
                while cli_atual.ant != None:
                    caminho.insert(0, cli_atual)
                    cli_atual = cli_atual.ant

                caminho.insert(0, origem)
                return caminho

        print("Sem caminho encontrado")
        return
