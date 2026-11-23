
from dataclasses import dataclass
from functools import partial
from math import inf
import heapq
import itertools

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
        self.__heap = []
        self.__counter = itertools.count()

    def get_time_cells(self):
        return [entry[2] for entry in sorted(self.__heap)]

    def schedule(self, cell):
        cell.time = self.get_current_time() + cell.time
        heapq.heappush(self.__heap, (cell.time, next(self.__counter), cell))

    def next_time(self):
        return self.__heap[0][0] if self.__heap else inf

    def pop_due_now(self):
        due = []
        while self.__heap and self.__heap[0][0] == self.__clock:
            due.append(heapq.heappop(self.__heap)[2])
        return due

    def get_current_time(self):
        return self.__clock

    def set_current_time(self, time):
        self.__clock = time