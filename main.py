from functools import partial

from src import Executive
from src.ApplicationSpecific import ActivityType, Client, NetworkModel, Packet
from src.ApplicationSpecific.Router import Router
from src.Engine import Engine, TimeCell



engine = Engine()

router = Router()
network_model = NetworkModel.NetworkModel(router=router, engine=engine)

executive = Executive.Executive(engine, network_model)



client = Client.Client(name="Client1", data_structure="SkipList")
network_model.clients.append(client)

client = Client.Client(name="Client2", data_structure="SkipList")
network_model.clients.append(client)



packet = Packet.Packet(data="Packet1")
client = network_model.clients[0]
client.get_packet_list().add_packet(packet_id=1, packet=packet)
packet = Packet.Packet(data="Packet2")
client.get_packet_list().add_packet(packet_id=2, packet=packet)




activity_type = ActivityType.ActivityType.C_START_PROCESSING_SOURCE



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
    time = 2,
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
executive.run(until = 10)
print("\nFim da simulação...\n==============================")


print("Resultado dos Clients após simulação:")
for cli in network_model.clients:
    print(f"Client: {cli.get_name()}")
    print(f"Queue: {[item.get_packet().get_data() for item in cli.get_job_queue()]}")