import random
from functools import partial

from src.Executive import Executive
from src.ApplicationSpecific.ActivityType import ActivityType
from src.ApplicationSpecific.Client import Client
from src.ApplicationSpecific.Information import Info
from src.ApplicationSpecific.NetworkModel import NetworkModel
from src.ApplicationSpecific.Packet import Packet
from src.ApplicationSpecific.Router import Router
from src.Engine import Engine, TimeCell


# ===== modo rápido: silencia os prints da simulação (o fast.py continua imprimindo) =====
import src.Executive as _executive_mod
import src.ApplicationSpecific.NetworkModel as _network_mod
import src.ApplicationSpecific.Router as _router_mod

def _sem_print(*args, **kwargs):
    pass

for _mod in (_executive_mod, _network_mod, _router_mod):
    _mod.print = _sem_print
# ========================================================================================

# ====================================
SEED = 42          
#SEED = random.randrange(1_000_000) #basta comentar essa linha para fundamentação em materiais e metodos    
NUM_CLIENTES   = 10         
NUM_PACOTES    = 1000
WINDOW_SIZE    = 500          
BUFFER_SIZE    = 500         
DATA_STRUCTURE = "LinkedList" #SkipList | LinkedList

LATENCIA       = 123.5
PERDA          = 0.01
VARIANCIA      = 0.25

UNTIL = 60_000_000 #1 minuto de tempo máximo
# ===========================================================


random.seed(SEED)

engine = Engine()

router = Router()
network_model = NetworkModel(router=router, engine=engine)

executive = Executive(engine, network_model)


#clientes 
for i in range(NUM_CLIENTES):
    if i == 0:
        client = Client(name=f"Client{i+1}", data_structure=DATA_STRUCTURE,
                        window_size=WINDOW_SIZE, buffer_size=BUFFER_SIZE)
    else:
        client = Client(name=f"Client{i+1}", data_structure=DATA_STRUCTURE)
    network_model.clients.append(client)


# pacotes
source = network_model.clients[0]
for packet_id in range(NUM_PACOTES):
    source.get_application_memory().add_packet(
        packet_id=packet_id,
        packet=Packet(data=f"Pacote{packet_id}")
    )


#adjacências
for a, b in zip(network_model.clients, network_model.clients[1:]):
    a.add_adj(b, Info(latencia=LATENCIA, perda=PERDA, variancia=VARIANCIA))
    b.add_adj(a, Info(latencia=LATENCIA, perda=PERDA, variancia=VARIANCIA))


activity_type = ActivityType.C_LOAD_PACKET

#atividades
print("[INICIALIZAÇÃO] Registrando eventos de teste...\n")
for packet_id in range(NUM_PACOTES):
    cell = TimeCell(
        name = f"B_arrival {source.get_name()} Packet{packet_id}",
        time = 1,
        action = partial(
            executive.network_model.B_arrival,
            source,
            packet_id,
            activity_type
        )
    )
    engine.schedule(cell)


print("[INICIALIZAÇÃO] Topologia:")
print("  " + " <-> ".join(c.get_name() for c in network_model.clients))
print(f"  pacotes={NUM_PACOTES} | janela={WINDOW_SIZE} | buffer={BUFFER_SIZE} | "
      f"latência={LATENCIA} | perda={PERDA} | estrutura={DATA_STRUCTURE} | seed={SEED}")

print("\n[INICIALIZAÇÃO] Eventos agendados:")
for time_cell in engine.get_time_cells():
    print(f"  - {time_cell.name} | horário={time_cell.time:.2f}")

print()

print("\n========== Início da simulação ==========\n")

executive.run(until=UNTIL)

print("\n========== Fim da simulação ==========\n")


print("[RESULTADO] Estado final dos clientes:")
for cli in network_model.clients:
    print(f"\n[CLIENTE] {cli.get_name()}")

    application_packets = cli.get_application_memory().get_all_packets()
    print(f"  Memória de aplicação: {len(application_packets)} pacote(s)")

    protocol_buffer = cli.get_protocol_buffer()
    print(f"  Buffer de protocolo: {protocol_buffer.get_size()} pacote(s)")
    print(
        f"  Janela de retransmissão: base={cli.get_current_idx()}, "
        f"confirmações={cli.get_retransmission_window()}"
    )

    queue = cli.get_job_queue()
    print(f"  Fila de atividades: {len(queue)} item(ns)")
    for queue_item in queue:
        print(f"    #{queue_item.get_packet_id()} | {queue_item.get_activity_type().name}")


# verificação de entrega no destino
destination = network_model.clients[-1]
entregues = []
corrompidos = []
faltando = []
for packet_id in range(NUM_PACOTES):
    packet = destination.get_protocol_buffer().get_packet(packet_id)["packet"]
    if packet is None:
        faltando.append(packet_id)
    elif packet.get_data() != f"Pacote{packet_id}":
        corrompidos.append(packet_id)
    else:
        entregues.append(packet_id)


print("\n[RESULTADO] Métricas da rede:")
print(f"  Tempo final da simulação: {engine.get_current_time():.2f}")
print(f"  Pacotes confirmados na origem (base da janela): {source.get_current_idx()}/{NUM_PACOTES}")
print(f"  Pacotes íntegros no destino: {len(entregues)}/{NUM_PACOTES}")
if faltando:
    print(f"  Pacotes ausentes ou None no destino: {faltando}")
if corrompidos:
    print(f"  Pacotes com conteúdo diferente: {corrompidos}")
print(f"  Pacotes perdidos: {network_model.get_total_lost_packets()}")
print(f"  Tempo total de processamento: {network_model.get_total_processing_time():.2f}")

if source.get_current_idx() == NUM_PACOTES and len(entregues) == NUM_PACOTES:
    print("\n[RESULTADO] OK: todos os pacotes foram confirmados e entregues íntegros.")
else:
    print("\n[RESULTADO] ATENÇÃO: a simulação terminou sem confirmar ou entregar todos os pacotes.")