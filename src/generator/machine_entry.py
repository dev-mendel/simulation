__author__ = "Petr Kohout <xkohou14@stud.fit.vutbr.cz>"
__date__ = "$29.8.2020 10:43:10$"

from debug.iniLoader import IniLoader
from utils.vector import Vector
from objects.cyanobacteria import CyanoBacteria
from generator.generator import Generator


class MachineEntry(Generator):

    def __init__(self, INI_FILE):
        super().__init__(INI_FILE, "machine")

        env = INI_FILE+"."+"environment"+"."

        self.ini_file = INI_FILE

        self.size_x = int(IniLoader.load(self.ini + "size_x")) / 10.0  # cm
        self.size_y = int(IniLoader.load(self.ini + "size_y")) / 10.0  # cm
        self.size_z = int(IniLoader.load(self.ini + "size_z")) / 10.0  # cm

        self.speed = float(IniLoader.load(self.ini + "speed")) * 100.0 / 1000.0  # cm/ms

        self.entry_x = int(IniLoader.load(self.ini + "entry_x")) / 10.0  # cm
        self.entry_y = int(IniLoader.load(self.ini + "entry_y")) / 10.0  # cm

        self.cyanos = float(IniLoader.load(env + "density")) # units / cm3

        self.logger.log("created", showInConsole=True)

    def generate(self, time_step):
        """
        :param time_step: time [millisecond] in which  water flowed into the machine
        :return: [Object]
        """
        volume = self.entry_x * self.entry_y * (self.speed * time_step)  # cm3
        cyanos_num = int(volume * self.cyanos)  # number of units

        speed_mm_ms = self.speed * 10.0  # mm/ms

        cyanos = []
        base_pos_vec = Vector(self.entry_x - 5, self.entry_y - 3, 50)
        base_dir_vec = Vector(speed_mm_ms * time_step, 0, 0)

        for c in range(cyanos_num):
            cyanos.append(CyanoBacteria(self.ini_file, base_pos_vec, base_dir_vec))

        self.logger.log("Generated: " + str(cyanos_num))
        return cyanos
