
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
        self.clock = 0
        self.time_cells = []

    def add_time_cell(self, cell):
        self.time_cells.append(cell)

    def schedule(self, cell, time):
        cell.time = time

    def next_time(self):
        return min(
            (cell.time for cell in self.time_cells),
            default=inf
        )

    def cells_due_now(self):
        return [
            cell
            for cell in self.time_cells
            if cell.time == self.clock
        ]

    def get_current_time(self):
        return self.clock