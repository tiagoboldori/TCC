class Conection:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.index = 0
      


class Manager:
    def __init__(self):
        #mapa O(1)
        self.__connections = {}
        self.__packages = [Package(str(i)) for i in range(0,900)]

    def add_connection(self, address, port):
        connection = Conection(address, port)
        self.__connections[f"{address}:{port}"] = connection

    def get_connections(self):
        return self.__connections

    def exist_connection(self, address, port):
        try:
            t = self.__connections[f"{address}:{port}"]
            return True
        except:
            return False
        
        #dps testar se é mais rapido usar o try catch ou o in
        return f"{address}:{port}" in self.__connections
    
    def get_connection(self, address, port):
        return self.__connections[f"{address}:{port}"]
    
    def remove_connection(self, address, port):
        del self.__connections[f"{address}:{port}"]

    def get_package_data(self, index):
        try:
            return self.__packages[index].data
        except IndexError:
            return None
    def get_packages(self):
        return self.__packages

class Package:
    def __init__(self, data):
        self.data = data
        self.created_at = None


