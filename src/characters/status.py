from typing import Tuple
from enum import Enum


class Direction(Enum):
    LEFT = 0
    RIGHT = 1


class State(Enum):
    IDLE = 0
    JUMP = 1


class Status:
    def __init__(self):
        self.state = State.IDLE
        self.direction = Direction.RIGHT

    def get_status(self) -> Tuple[Direction, State]:
        return (self.direction, self.state)

    def set_direction(self, direction: Direction):
        self.direction = direction

    def set_state(self, state: State):
        self.state = state
