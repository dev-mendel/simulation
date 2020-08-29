__author__ = "Petr Kohout <xkohou14@stud.fit.vutbr.cz>"
__date__ = "$29.8.2020 12:53:10$"

from typing import List, Tuple
import numpy as np

from debug.iniLoader import IniLoader
from debug.logger import Loggable
#from objects.object import Object
from utils.vector import Vector


class Grid:
    """
    Singleton class for storing object in machine
    """
    pool = None

    def __init__(self):
        if not Grid.pool:
            raise EnvironmentError("Pool is not set, please run somewhere Grid.initPool before you work with that")

    @staticmethod
    def initPool(INI_FILE):
        if not Grid.pool:
            Grid.pool = Grid.__Grid(INI_FILE)

    class __Grid(Loggable):
        def __init__(self, INI_FILE):
            super().__init__()

            env = INI_FILE + "." + "environment" + "."
            machine = INI_FILE + "." + "machine" + "."

            self.size_x = int(IniLoader.load(machine + "size_x"))  # mm
            self.size_y = int(IniLoader.load(machine + "size_y"))  # mm
            self.size_z = int(IniLoader.load(machine + "size_z"))  # mm

            self.grid_edge_size = int(IniLoader.load(env + "grid_size"))  # mm

            self.grid = [[[Grid.Stack() for k in range(self.size_x // self.grid_edge_size)]
                                for j in range(self.size_y // self.grid_edge_size)]
                                    for i in range(self.size_z // self.grid_edge_size)]
            # self.grid = np.empty((int(self.size_x / self.grid_edge_size),
            #                      int(self.size_y / self.grid_edge_size),
            #                      int(self.size_z / self.grid_edge_size), S))

            # for x in range(int(self.size_x / self.grid_edge_size)):
            #    for y in range(int(self.size_y / self.grid_edge_size)):
            #        for z in range(int(self.size_z / self.grid_edge_size)):
            #            self.grid[x][y][z] = []

            self.logger.log("created, pool has: " + str(len(self.grid)))

        def set(self, o):
            """
            :param o: Object
            :return:
            """
            (x, y, z) = self.to_grid_pos(o.position)
            if not self.in_range(o.position):
                self.logger.log("couldn't store object " + str(o.id) + " at position " + str(o.position), showInConsole=True)
            else:
                self.grid[x][y][z].add(o)

        def in_range(self, pos):
            (x, y, z) = self.to_grid_pos(pos)
            s = self.grid_edge_size
            # return x < 0 or y < 0 or z < 0 or x >= self.size_x // s or y >= self.size_y // s or z >= self.size_z // s
            return x in range(x // s) and y in range(y // s) and z in range(z // s)

        def remove(self, o):
            """
            :param o: Object
            :return:
            """
            (x, y, z) = self.to_grid_pos(o.position)
            if not self.in_range(o.position):
                self.logger.log("couldn't remove object " + str(o.id) + " at position " + str(o.position), showInConsole=True)
            else:
                self.grid[x][y][z].remove(o)

        def to_grid_pos(self, pos: Vector):
            (x, y, z) = pos.v
            return x // self.grid_edge_size, y // self.grid_edge_size, z // self.grid_edge_size

        def compute_collisions(self):
            for x in range(int(self.size_x / self.grid_edge_size)):
                for y in range(int(self.size_y / self.grid_edge_size)):
                    for z in range(int(self.size_z / self.grid_edge_size)):
                        cell_stack = self.grid[x][y][z]
                        if len(cell_stack.arr):
                            map(lambda e: e[0].collision(e[1]), self.get_pairs(cell_stack.arr))

        def get_pairs(self, stack):
            """
            :param stack: [Object]
            :return: List[Tuple[Object, Object]]
            """
            pairs = []
            for i, item in enumerate(stack):
                for i2, item2 in enumerate(stack[i+1:]):
                    pairs.append((item, item2))

            return pairs

    class Stack:
        def __init__(self):
            self.arr = []

        def add(self, el):
            self.arr.append(el)

        def remove(self, el):
            for i, item in enumerate(self.arr):
                if item.id == el.id:
                    del self.arr[i]
