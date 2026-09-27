from src.Engine import TimeCell, Engine
from functools import partial
from math import inf

class Executive:
    def __init__(self, engine, model):
        self.engine = engine
        self.network_model = model

    def run(self, until=100):
        while True:

            #pega o time cell de menor tempo (evento mais proximo)
            next_time = self.engine.next_time()

            
            #Avanço de tempo
            #======= A Phase ========
            if self.engine.get_current_time() >= until:
                break

            if next_time == inf:
                break

            self.engine.clock = next_time

            print("Simulation Clock = " + str(self.engine.get_current_time()))

            
            # Execução de B activities
            #======= B Phase ========
            print("Executing B activities...")
            due_cells = self.engine.cells_due_now()
            for cell in due_cells:
                print(f"Executing cell: {cell.name} at time {cell.time} ")
                cell.action()
                cell.time = inf



            # Execução de C activities
            #======= C Phase ========
            print("Executing C activities...")
            self.network_model.C_process_all()