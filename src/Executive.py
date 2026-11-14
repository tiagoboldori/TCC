from src.Engine import TimeCell, Engine
from functools import partial
from math import inf

class Executive:
    def __init__(self, engine, model):
        self.engine = engine
        self.network_model = model

    def run(self, until=1000):
        while True:

            #pega o time cell de menor tempo (evento mais proximo)
            next_time = self.engine.next_time()

            
            #Avanço de tempo
            #======= A Phase ========
            if self.engine.get_current_time() >= until:
                break

            if next_time == inf:
                break

            self.engine.set_current_time(next_time)

            print(f"\n========== Relógio da simulação: {self.engine.get_current_time():.2f} ==========")

            
            # Execução de B activities
            #======= B Phase ========
            print("\n[Fase B] Executando eventos agendados...")
            due_cells = self.engine.cells_due_now()
            for cell in due_cells:
                print(f"[Fase B][EVENTO] {cell.name} | horário={cell.time:.2f}.")
                cell.action()
                cell.time = inf



            # Execução de C activities
            #======= C Phase ========
            print("\n[Fase C] Processando atividades dos clientes...")
            self.network_model.C_process_all()