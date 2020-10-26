__author__ = "Petr Kohout <xkohou14@stud.fit.vutbr.cz>"
__date__ = "$29.8.2020 10:43:10$"

from debug.iniLoader import IniLoader
from utils.vector import Vector
from utils.pool import Grid
from utils.simulation import SimulationManager
from generator.generator import Generator
from objects.object import Object, ObjectTypes


class MachineExit(Generator):

    def __init__(self, INI_FILE):
        super().__init__(INI_FILE, "machine")

        env = INI_FILE+"."+"environment"+"."

        self.ini_file = INI_FILE

        self.size_x = int(IniLoader.load(self.ini + "size_x"))  # mm
        self.size_y = int(IniLoader.load(self.ini + "size_y"))  # mm
        self.size_z = int(IniLoader.load(self.ini + "size_z"))  # mm

        self.speed = float(IniLoader.load(self.ini + "speed")) * 100.0 / 1000.0  # mm/ms

        self.exit_x = int(IniLoader.load(self.ini + "exit_x"))  # mm
        self.exit_y = int(IniLoader.load(self.ini + "exit_y"))  # mm

        #  we wanna make it in the middle of wall
        self.exit_x_start = int((self.size_y / 2) - (self.exit_x / 2))
        self.exit_y_start = int((self.size_x / 2) - (self.exit_y / 2))

        self.logger.log("created " + str(self), showInConsole=True)

    def __str__(self):
        return "( \nspeed:" + str(self.speed) \
               + " \nsize_x:" + str(self.size_x) \
               + " \nsize_y:" + str(self.size_y) \
               + " \nsize_z:" + str(self.size_z) \
               + " \nexit_x:" + str(self.exit_x) \
               + " \nexit_y:" + str(self.exit_y) \
               + "\n)"

    def generate(self, time_step):
        """
        :param time_step: time [millisecond] in which  water flowed into the machine
        :return: [Object]
        """
        volume = self.exit_x * self.exit_y * (self.speed * time_step)  # cm3
        grid_distance = int(self.speed * time_step * 10)  # mm
        x_range = range(self.size_x - grid_distance, self.size_x)
        y_range = range(self.exit_x_start, self.exit_x_start + self.exit_x)
        z_range = range(self.exit_y_start, self.exit_y_start + self.exit_y)

        cyanos = []
        deleted = 0
        grid = Grid().pool

        for i, (item) in enumerate(SimulationManager().manager.objects):
            item: Object = item
            if item.type == ObjectTypes.CYANO_BACTERIA:
                x, y, z = item.position.v
                if x in x_range and y in y_range and z in z_range:
                    grid.remove(item)
                    del SimulationManager().manager.objects[i]
                    deleted += 1

        self.logger.log("Destroyed: " + str(deleted), showInConsole=True)
        return []
