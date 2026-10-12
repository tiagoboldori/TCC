
from dataclasses import dataclass
from functools import partial
from math import inf


@dataclass
class TimeCell:
    name: str
    time: float = inf
    action: callable = None

    def __str__(self):
        return f"TimeCell(name={self.name}, time={self.time})"


class Engine:

    def __init__(self):
        self.__clock = 0
        self.__time_cells = []

    def get_time_cells(self):
            return self.__time_cells
    
    def set_time_cells(self, time_cells):
        self.__time_cells = time_cells

    def add_time_cell(self, cell):
        self.__time_cells.append(cell)



    def schedule(self, cell):
        cell.time = self.get_current_time() + cell.time
        self.add_time_cell(cell)

    def next_time(self):
        return min(
            (cell.time for cell in self.__time_cells),
            default=inf
        )

    def cells_due_now(self):
        return [
            cell
            for cell in self.__time_cells
            if cell.time == self.__clock
        ]

    def get_current_time(self):
        return self.__clock

    def set_current_time(self, time):
        self.__clock = time


    