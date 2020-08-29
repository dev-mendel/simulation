__author__ = "Petr Kohout <xkohou14@stud.fit.vutbr.cz>"
__date__ = "$29.8.2020 16:05:10$"

from objects.object import Object, ObjectTypes
from objects.ball import Ball
from utils.vector import Vector


class CyanoBacteria(Object):

    def __init__(self, INI_FILE: str, pos: Vector, dir: Vector):
        super().__init__(INI_FILE=INI_FILE, position=pos, direction=dir)

        self.type = ObjectTypes.CYANO_BACTERIA
        self.docker: Object = None

    def move(self, direction=None):
        if self.docker:  # if it is docked
            super(CyanoBacteria, self).move(self.docker.direction)
        else:
            super(CyanoBacteria, self).move()

    def collision(self, o: Object):
        if o.type == ObjectTypes.CYANO_BACTERIA:
            self.direction.average(o.direction)
            o.direction.average(self.direction)
        elif o.type == ObjectTypes.BALL:
            o: Ball = o

        elif o.type == ObjectTypes.BUBBLE:  # it is strong bubble :D
            self.direction.average(o.direction)
            self.direction.average(o.direction)
        else:
            raise EnvironmentError("Cannot make collision with UNKNOWN type")
