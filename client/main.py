import socket

HOST = '192.168.29.5'
PORT = 65432
BUFFER_SIZE = 128


SERVER_ADDRESS = '192.168.29.5'
SERVER_PORT = 65000




print("Iniciando Cliente UDP...")

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client_socket.bind((HOST,PORT))
    print(f"Socket vinculada em {HOST}:{PORT}")
    print(f"Enviando dados para {SERVER_ADDRESS}:{SERVER_PORT}: CONN")
    

    #Handshake de conexão
    client_socket.sendto("CONN".encode('utf-8'), (SERVER_ADDRESS, SERVER_PORT))
    try:
        data, server_address = client_socket.recvfrom(BUFFER_SIZE)
        decoded_data = data.decode('utf-8')
        if decoded_data == "OK":
            print(f"Conexão estabelecida com o servidor: {server_address}")
        else:
            client_socket.close()
            raise Exception("Resposta inesperada do servidor. Conexão encerrada.")


        #Loop principal do programa
        while True:
            data, client_address = client_socket.recvfrom(BUFFER_SIZE)
            print(data.decode('utf-8'))
            

    except socket.error as e:
        print(f"aviso:{e}")


except socket.error as e:
    print(f"erro de Socket: {e}")

except KeyboardInterrupt:
    print("Servidor encerrado.")

finally:
    client_socket.close()
    print("Cliente UDP fechado.")