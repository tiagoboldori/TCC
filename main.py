from functools import partial

from src.Executive import Executive
from src.ApplicationSpecific.ActivityType import ActivityType
from src.ApplicationSpecific.Client import Client
from src.ApplicationSpecific.Information import Info
from src.ApplicationSpecific.NetworkModel import NetworkModel
from src.ApplicationSpecific.Packet import Packet
from src.ApplicationSpecific.Router import Router
from src.Engine import Engine, TimeCell



engine = Engine()

router = Router()
network_model = NetworkModel(router=router, engine=engine)

executive = Executive(engine, network_model)



client1 = Client(name="Client1", data_structure="SkipList", window_size=2)
network_model.clients.append(client1)

client1.get_application_memory().add_packet(packet_id=0, packet=Packet(data="Abobrinha"))
client1.get_application_memory().add_packet(packet_id=1, packet=Packet(data="Pessego"))


client2 = Client(name="Client2", data_structure="SkipList")
network_model.clients.append(client2)


client1.add_adj(client2, Info(latencia=5, perda=0.15, variancia=0.25))
client2.add_adj(client1, Info(latencia=5, perda=0.15, variancia=0.25))


#packet = Packet.Packet(data="Packet2")
#client.get_packet_list().add_packet(packet_id=2, packet=packet)




activity_type = ActivityType.C_LOAD_PACKET



print("[INICIALIZAÇÃO] Registrando eventos de teste...\n")
cell = TimeCell(
    name = "B_arrival Client1 Packet1",
    time = 1,
    action = partial(
        executive.network_model.B_arrival,
        network_model.clients[0],
        0,
        activity_type
    )
)
engine.schedule(cell)

cell = TimeCell(
    name = "B_arrival Client1 Packet2",
    time = 1,
    action = partial(
        executive.network_model.B_arrival,
        network_model.clients[0],
        1,
        activity_type
    )
)
engine.schedule(cell)



print("[INICIALIZAÇÃO] Eventos agendados:")

for time_cell in engine.get_time_cells():
    print(f"  - {time_cell.name} | horário={time_cell.time:.2f}")

print()

print("\n========== Início da simulação ==========\n")

executive.run(until=1000)

print("\n========== Fim da simulação ==========\n")


print("[RESULTADO] Estado final dos clientes:")
for cli in network_model.clients:
    print(f"\n[CLIENTE] {cli.get_name()}")

    application_packets = cli.get_application_memory().get_all_packets()
    print(
        "  Memória de aplicação: "
        f"{application_packets if application_packets else 'vazia'}"
    )
    protocol_buffer = cli.get_protocol_buffer()
    try:
        protocol_packets = protocol_buffer.get_all_packets()
    except AttributeError as error:
        print(
            f"  Buffer de protocolo ({protocol_buffer.get_size()} pacote(s)): "
            f"erro ao listar conteúdo ({error})"
        )
    else:
        print(
            f"  Buffer de protocolo ({protocol_buffer.get_size()} pacote(s)): "
            f"{protocol_packets if protocol_packets else 'vazio'}"
        )
    print(
        f"  Janela de retransmissão: base={cli.get_current_idx()}, "
        f"confirmações={cli.get_retransmission_window()}"
    )

    queue = cli.get_job_queue()
    print(f"  Fila de atividades ({len(queue)}):")
    if not queue:
        print("    (vazia)")

    for queue_item in queue:
        packet_id = queue_item.get_packet_id()
        packet_info = cli.get_protocol_buffer().get_packet(packet_id)
        packet = packet_info["packet"]
        packet_data = packet.get_data() if packet else "<sem pacote no buffer>"
        print(
            f"    #{packet_id} | {queue_item.get_activity_type().name} "
            f"| dado={packet_data}"
        )

print("\n[RESULTADO] Métricas da rede:")
print(f"  Tempo final da simulação: {engine.get_current_time():.2f}")
print(f"  Pacotes perdidos: {network_model.get_total_lost_packets()}")
print(f"  Tempo total de processamento: {network_model.get_total_processing_time():.2f}")