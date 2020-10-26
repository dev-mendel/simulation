__author__ = "Petr Kohout <xkohou14@stud.fit.vutbr.cz>"
__date__ = "$29.8.2020 16:21:10$"

from objects.object import Object, ObjectTypes
#from objects.cyanobacteria import CyanoBacteria
from utils.vector import Vector
from utils.simulation import SimulationManager
from debug.iniLoader import IniLoader


class Ball(Object):

    def __init__(self, INI_FILE: str, pos: Vector, dir: Vector):
        super().__init__(INI_FILE=INI_FILE, position=pos, direction=dir)

        self.ini = self.ini + "ball."

        self.capacity = int(IniLoader.load(self.ini + "capacity"))
        self.grid_size = int(IniLoader.load(self.ini + "grid_size"))
        self.avg_docking = int(IniLoader.load(self.ini + "avg_docking"))
        self.destroyed = 0  # nuber of destroyed cells

        self.cyanos = []  # : [CyanoBacteria]

        self.type = ObjectTypes.BALL

    def move(self, direction=None):
        self.destroyed = 0  # count number of destroyed cells
        for i, item in enumerate(self.cyanos):
            self.cyanos[i]["time"] -= SimulationManager().manager.time_step
            if self.cyanos[i]["time"] <= 0:
                self.undock(self.cyanos[i]["obj"])
                self.destroyed += 1
        super(Ball, self).move()


    def collision(self, o: Object):
        if o.type == ObjectTypes.CYANO_BACTERIA:  # : CyanoBacteria
            self.dock(o)
        elif o.type == ObjectTypes.BALL:
            self.direction.average(o.direction)
            o.direction.average(self.direction)
        elif o.type == ObjectTypes.BUBBLE:  # it is strong bubble :D
            self.direction.average(o.direction)
            self.direction.average(o.direction)
        else:
            raise EnvironmentError("Cannot make collision with UNKNOWN type")

    def dock(self, o):
        """
        :param o: CyanoBacteria
        :return:
        """
        if len(self.cyanos) < self.capacity:
            o.docker = self
            self.cyanos[o.id] = {
                "time": self.avg_docking,    # time ticking
                "obj": o
            }
        else:
            self.logger.log(str(self.id) + " is fully docked")

    def undock(self, o):
        """
        :param o: CyanoBacteria
        :return:
        """
        if len(self.cyanos) > 0:
            o.docker = None
            del self.cyanos[o.id]

    def json_str(self):
        return "{" \
                    + '"type": "' + str(self.type) + '", ' \
                    + '"id": ' + str(self.id) + ", " \
                    + '"docked": ' + str(len(self.cyanos)) + ", " \
                    + '"destroyed": ' + str(self.destroyed) + ", " \
                    + '"pos": ' + str(self.position.json_str()) \
               + "}"
