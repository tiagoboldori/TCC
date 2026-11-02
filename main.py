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



client1 = Client(name="Client1", data_structure="SkipList")
network_model.clients.append(client1)

client1.get_application_memory().add_packet(packet_id=1, packet=Packet(data="Abobrinha"))
client1.get_application_memory().add_packet(packet_id=2, packet=Packet(data="Pessego"))


client2 = Client(name="Client2", data_structure="SkipList")
network_model.clients.append(client2)


client1.add_adj(client2, Info(latencia=15, perda=0.5, variancia=0.2))


#packet = Packet.Packet(data="Packet2")
#client.get_packet_list().add_packet(packet_id=2, packet=packet)




activity_type = ActivityType.C_LOAD_PACKET



print("Inserindo agendamentos arbitrários para testes...\n")
cell = TimeCell(
    name = "B_arrival Client1 Packet1",
    time = 1,
    action = partial(
        executive.network_model.B_arrival,
        network_model.clients[0],
        1,
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
        2,
        activity_type
    )
)
engine.schedule(cell)



print("Time Cells/Agendamentos existentes:")

for time_cell in engine.get_time_cells():
    print(time_cell)

print("\n...\n")

print("Iniciando Simulação... \n==============================")

executive.run(until=1000)

print("\nFim da simulação...\n==============================")


print("Resultado dos Clients após simulação:\n==============================")
for cli in network_model.clients:
    print("__________________________")
    print(f"Client: {cli.get_name()}")
    txt = ""
    while cli.get_job_queue():
        queue_item = cli.get_job_queue().popleft()
        txt+= str(queue_item.get_packet_id()) + " " + queue_item.get_activity_type().name + " "+cli.get_protocol_buffer().get_packet(queue_item.get_packet_id())['packet'].get_data() + " | "
    print(f"Job Queue: {txt}")
    print(f"Packets: {cli.get_protocol_buffer().get_all_packets()}")

print("\nResultado do Router após simulação:\n==============================")
print(f"Lost Packets: {network_model.get_total_lost_packets()}")
print(f"Processing Time: {network_model.get_total_processing_time()}")