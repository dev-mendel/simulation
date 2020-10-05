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

            (x_max, y_max, z_max) = self.max_range()

            self.logger.log("creating pool: " + str(self.size_x * self.size_y * self.size_z))

            self.grid = [[[Grid.Stack() for k in range(z_max)]
                                for j in range(y_max)]
                                    for i in range(x_max)]
            # self.grid = np.empty((int(self.size_x / self.grid_edge_size),
            #                      int(self.size_y / self.grid_edge_size),
            #                      int(self.size_z / self.grid_edge_size), S))

            # for x in range(int(self.size_x / self.grid_edge_size)):
            #    for y in range(int(self.size_y / self.grid_edge_size)):
            #        for z in range(int(self.size_z / self.grid_edge_size)):
            #            self.grid[x][y][z] = []
            self.number_of_objects = 0

            self.logger.log("created, pool has: " + str(len(self.grid))+" "+str(len(self.grid[0]))+" "+str(len(self.grid[0][0]))
                            +"\n"+str(x_max)+","+str(y_max)+","+str(z_max), showInConsole=True)

        def set(self, o):
            """
            :param o: Object
            :return:
            """
            (x, y, z) = self.to_grid_pos(o.position)
            if not self.in_range(o.position):
                self.logger.log("couldn't store object " + str(o.id) + " at position " + str(o.position), showInConsole=True)
                exit(1)
            else:
                try:
                    self.grid[x][y][z].add(o)
                    self.number_of_objects += 1
                except IndexError:
                    self.logger.log("Out of range " + str(o.id) + " at position " + str(o.position),
                                    showInConsole=True)
                    exit(1)

        def max_range(self):
            """
            :return: Tuple [x, y, z] with max walls positions
            """
            s = self.grid_edge_size
            return self.to_grid_pos(Vector(self.size_x // s, self.size_y // s, self.size_z // s))

        def in_range(self, pos):
            (x, y, z) = self.to_grid_pos(pos)
            (x_max, y_max, z_max) = self.max_range()
            s = self.grid_edge_size
            # return x < 0 or y < 0 or z < 0 or x >= self.size_x // s or y >= self.size_y // s or z >= self.size_z // s
            return x in range(x_max) and y in range(y_max) and z in range(z_max)

        def wall_collision_next_position(self, pos, dir):
            """
            :param pos: Vector
            :param dir: Vector direction of object
            :return: Vector, Vector: new position of object after wall collision, and new direction
            """
            (x, y, z) = self.to_grid_pos(pos)

            (x_dir, y_dir, z_dir) = dir.v
            (x_max, y_max, z_max) = self.max_range()
            if x not in range(x_max):  # collision in X axis
                x_dir = -x_dir
                if x < 0:
                    x = abs(x) % x_max
                elif x == x_max:
                    x = x_max - 1
                else:
                    over = x % x_max
                    x = x_max - over
            elif y not in range(y_max):  # collision in Y axis
                y_dir = -y_dir
                if y < 0:
                    y = abs(y) % y_max
                elif y == y_max:
                    y = y_max - 1
                else:
                    over = y % y_max
                    y = y_max - over
            elif z not in range(z_max):  # collision in Z axis
                z_dir = -z_dir
                if z < 0:
                    z = abs(z) % z_max
                elif z == z_max:
                    z = z_max - 1
                else:
                    over = z % z_max
                    z = z_max - over

            return Vector(x, y, z), Vector(x_dir, y_dir, z_dir)

        def remove(self, o):
            """
            :param o: Object
            :return:
            """
            (x, y, z) = self.to_grid_pos(o.position)
            if not self.in_range(o.position):
                self.logger.log("couldn't remove object " + str(o.id) + " at position " + str(o.position) + " " + str(self), showInConsole=True)
                exit(1)
            else:
                try:
                    self.grid[x][y][z].remove(o)
                    self.number_of_objects -= 1
                except IndexError:
                    self.logger.log("Out of range " + str(o.id) + " at position " + str(o.position),
                                    showInConsole=True)
                    exit(1)

        def to_grid_pos(self, pos: Vector):
            (x, y, z) = pos.v
            return int(x // self.grid_edge_size), int(y // self.grid_edge_size), int(z // self.grid_edge_size)

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

        def __str__(self):
            return "pool has: " + str(len(self.grid))+" "+str(len(self.grid[0]))+" "+str(len(self.grid[0][0])) + " with " + str(self.number_of_objects) + " objects"

    class Stack:
        def __init__(self):
            self.arr = []

        def add(self, el):
            self.arr.append(el)

        def remove(self, el):
            for i, item in enumerate(self.arr):
                if item.id == el.id:
                    del self.arr[i]
