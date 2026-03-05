import socket
from etc import *
import time

HOST = '192.168.29.5'
PORT = 65000
BUFFER_SIZE = 128

manager = Manager()


print("Iniciando Servidor UDP...")

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setblocking(False)

    server_socket.bind((HOST,PORT))
    print(f"Socket vinculada em {HOST}:{PORT}")


    print("Aguardando conexão de cliente...")
    

    while True:
        client_address = None
        data = None

        try:
            data, client_address = server_socket.recvfrom(BUFFER_SIZE)
            decoded_data = data.decode('utf-8')

        except BlockingIOError:
            data = None
            client_address = None

        if (data!=None) and (client_address!=None):
            try:
                print(f"Dados recebidos de: {client_address}: {decoded_data}")

                if decoded_data == "CONN":
                    manager.add_connection(client_address[0], client_address[1])
                    print(f"Conexão recebida e mapeada: {client_address}")

                    response_message = "OK"
                
                    server_socket.sendto(response_message.encode('utf-8'), client_address)

            except socket.error as e:
                print(f"Erro ao enviar resposta para cliente: {e}")



        for i in manager.get_connections().values():
            time.sleep(0.01)
            try:
                send_data = manager.get_package_data(i.index)
                print(f"Enviando dados para {i.address}:{i.port}: {send_data}, pacote de numero {i.index}")
                if send_data != None:
                    res = server_socket.sendto(str.encode(send_data), (i.address, i.port))
                    if res > 0:
                        i.index += 1
                else:
                    print(f"Todos os pacotes foram enviados para {i.address}:{i.port}")

            except Exception as e:
                print(f"Erro ao enviar dados: {e}")
                pass
            
        

except socket.error as e:
    print(f"erro de Socket: {e}")

except KeyboardInterrupt:
    print("Servidor encerrado.")

finally:
    server_socket.close()
    print("Servidor fechado.")

