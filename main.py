from functools import partial

from src import Executive
from src.ApplicationSpecific import ActivityType, Client, NetworkModel, Packet
from src.ApplicationSpecific.Router import Router
from src.Engine import Engine, TimeCell



client = None
packet = None
activity_type = None


engine = Engine()

router = Router()
network_model = NetworkModel.NetworkModel(router=router, engine=engine)

executive = Executive.Executive(engine, network_model)



client = Client.Client(name="Client1")
packet = Packet.Packet(data="Packet1")
activity_type = ActivityType.ActivityType.START_PROCESSING
network_model.clients.append(client)


print("Inserindo agendamentos arbitrários para testes...\n")
cell = TimeCell(
    name = "A",
    time = executive.engine.get_current_time(),
    action = partial(
        executive.network_model.B_arrival,
        client,
        packet,
        activity_type
    )
)

packet = Packet.Packet(data="Packet2")

engine.add_time_cell(cell)

cell = TimeCell(
    name = "B",
    time = executive.engine.get_current_time() + 1,
    action = partial(
        executive.network_model.B_arrival,
        client,
        packet,
        activity_type
    )
)

engine.add_time_cell(cell)


print("Time Cells/Agendamentos existentes:")
for time_cell in engine.time_cells:
    print(time_cell)
print("\n...\n")

print("Iniciando Simulação... \n==============================")
executive.run(until = 10)
print("\nFim da simulação...\n==============================")


print("Resultado dos Clients após simulação:")
for cli in network_model.clients:
    print(f"Client: {cli.get_name()}")
    print(f"Queue: {[item.get_packet().get_data() for item in cli.get_queue()]}")