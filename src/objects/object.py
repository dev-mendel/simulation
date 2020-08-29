__author__ = "Petr Kohout <xkohou14@stud.fit.vutbr.cz>"
__date__ = "$29.8.2020 11:42:10$"

from abc import abstractmethod
from enum import Enum

from debug.logger import Loggable
from generator.ID import ID
from utils.vector import Vector
from utils.pool import Grid


class ObjectTypes(Enum):
    UNKNOWN = 1,
    CYANO_BACTERIA = 2,
    BALL = 3,
    BUBBLE = 4,


class Object(Loggable):

    def __init__(self, INI_FILE: str, position: Vector, direction: Vector):
        super().__init__()

        self.ini = INI_FILE + "."

        self.id = ID().getID()
        self.position = position
        self.direction = direction
        self.type = ObjectTypes.UNKNOWN
        Grid().pool.set(self)

    def move(self, direction=None):
        grid = Grid().pool
        grid.remove(self)
        if direction:
            self.position.plus(direction)
        else:
            self.position.plus(self.direction)
        grid.set(self)

    @abstractmethod
    def collision(self, o):
        pass
