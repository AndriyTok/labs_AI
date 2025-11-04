from enum import Enum


class CellType(Enum):
    EMPTY = 0
    OBSTACLE = -1
    START = 2
    END = 3
    PATH = 4


class OperatorType(Enum):
    FOUR_DIRECTIONS = "4 напрямки"
    EIGHT_DIRECTIONS = "8 напрямків (діагоналі)"
    COMBINED = "Комбінований"


class SearchResult:
    def __init__(self, path=None, cycles=0, time=0, operator=""):
        self.path = path
        self.cycles = cycles
        self.time = time
        self.operator = operator
        self.length = len(path) if path else 0
        self.found = path is not None
