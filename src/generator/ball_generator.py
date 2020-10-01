__author__ = "Petr Kohout <xkohou14@stud.fit.vutbr.cz>"
__date__ = "$29.8.2020 10:43:10$"

from debug.iniLoader import IniLoader
from utils.vector import Vector
from objects.ball import Ball
from generator.generator import Generator
import random


class BallGenerator(Generator):

    def __init__(self, INI_FILE):
        super().__init__(INI_FILE, "ball")

        self.ini_file = INI_FILE

        machine = INI_FILE + "." + "machine" + "."

        self.size_x = int(IniLoader.load(machine + "size_x"))  # mm
        self.size_y = int(IniLoader.load(machine + "size_y"))  # mm
        self.size_z = int(IniLoader.load(machine + "size_z"))  # mm

        self.balls = int(IniLoader.load(self.ini + "number"))

        self.balls_generated = False

        self.logger.log("created " + str(self), showInConsole=True)

    def __str__(self):
        return "( \nnumber:" + str(self.balls) \
               + " \nsize_x:" + str(self.size_x) \
               + " \nsize_y:" + str(self.size_y) \
               + " \nsize_z:" + str(self.size_z) \
               + " \ngenerated:" + str(self.balls_generated) \
               + "\n)"

    def generate(self, time_step):
        """
        :param time_step: time [millisecond] in which  water flowed into the machine
        :return: [Object]
        """
        if self.balls_generated:
            return []
        else:
            self.balls_generated = True

        balls = []
        base_pos_vec = Vector(self.size_x // 2, self.size_y // 2, self.size_z // 2)  # in the middle of entry
        base_dir_vec = Vector(0, 0, 1)
        for c in range(self.balls):
            balls.append(Ball(self.ini_file,
                                Vector(random.randint(self.size_x // 3, (self.size_x * 2) // 3),
                                       random.randint(self.size_y // 3, (self.size_y * 2) // 3),
                                       random.randint(self.size_z // 3, (self.size_z * 2) // 3)),
                                Vector(random.randint(self.size_x // 8, (self.size_x * 2) // 8),
                                       random.randint(self.size_y // 8, (self.size_y * 2) // 8),
                                       random.randint(self.size_z // 8, (self.size_z * 2) // 8))
                                ))

        self.logger.log("Generated: " + str(self.balls) + str(base_pos_vec)+ str(base_dir_vec), showInConsole=True)
        return balls
