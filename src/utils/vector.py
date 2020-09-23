__author__ = "Petr Kohout <xkohou14@stud.fit.vutbr.cz>"
__date__ = "$29.8.2020 12:09:10$"


class Vector:
    def __init__(self, x, y, z):
        self.v = (x, y, z)

    def plus(self, vec):
        x, y, z = self.v
        x2, y2, z2 = vec.v
        self.v = (x + x2, y + y2, z + z2)

    def minus(self, vec):
        x, y, z = self.v
        x2, y2, z2 = vec.v
        self.v = (x - x2, y - y2, z - z2)

    def average(self, vec):
        x, y, z = self.v
        x2, y2, z2 = vec.v
        self.v = ((x + x2) / 2, (y + y2) / 2, (z + z2) / 2)

    def __add__(self, other):
        x1, y1, z1 = self.v
        x2, y2, z2 = other.v
        return Vector(x1 + x2, y1 + y2, z1 + z2)

    def __sub__(self, other):
        x1, y1, z1 = self.v
        x2, y2, z2 = other.v
        return Vector(x1 - x2, y1 - y2, z1 - z2)

    def __neg__(self):
        x, y, z = self.v
        return Vector(-x, -y, -z)

    def __str__(self):
        x, y, z = self.v
        return "("+str(x)+", "+str(y)+", "+str(z)+")"

    def __repr__(self):
        return str(self)

    def __deepcopy__(self, memodict={}):
        x, y, z = self.v
        return Vector(x, y, z)

