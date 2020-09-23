

from objects.object import Object, ObjectTypes
#from objects.cyanobacteria import CyanoBacteria
from utils.vector import Vector
from utils.simulation import SimulationManager
from debug.iniLoader import IniLoader

class Bubble(Object):

    def __init__(self, INI_FILE: str, pos: Vector, dir: Vector):
        super().__init__(INI_FILE=INI_FILE, position=pos, direction=dir)

        self.ini = self.ini + "bubble."
        self.capacity = int(IniLoader.load(self.ini + "capacity"))
        self.grid_size = int(IniLoader.load(self.ini + "grid_size"))
        # self.avg_docking = int(IniLoader.load(self.ini + "avg_docking"))

        self.type = ObjectTypes.BUBBLE

    def collision(self, o: Object):
        # bubble still will go upway
        pass

    




