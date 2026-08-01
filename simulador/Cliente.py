class Cliente:
    def __init__(self, nome: str) -> None:
        # Nome é identificador de cliente
        self.__nome = nome
        self.__adj = []
        # Representação por lista de adjacencias.
        # adj = [[Cliente, Info], [Cliente2, Info2], ...]
        self.ant = None

    # Setter e Getter NOME
    def set_nome(self, nome: str) -> None:
        self.__nome = nome

    def get_nome(self) -> str | None:
        return self.__nome

    # Setter e Getter ADJACENCIAS
    def set_adj(self, adj: list) -> None:
        self.__adj = adj

    def add_adj(self, cliente, info):
        if [cliente, info] not in self.get_all_adj():
            self.__adj.append([cliente, info])

    def get_all_adj(self):
        return self.__adj

    def get_adj(self, cliente):
        for adj in self.get_all_adj():
            if adj[0] == cliente:
                return adj
