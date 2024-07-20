from enum import Enum
from random import choice


class Direction(Enum):
    LEFT = 0
    RIGHT = 1


class State(Enum):
    IDLE = 0
    JUMP = 1


class Status:
    def __init__(self):
        self.state = State.IDLE
        self.direction = choice([Direction.LEFT, Direction.RIGHT])

    def get_status(self) -> Tuple[Direction, State]:
        return (self.direction, self.state)
