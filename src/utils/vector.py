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

    def __str__(self):
        x, y, z = self.v
        return "("+str(x)+", "+str(y)+", "+str(z)+")"

    def get_line_vec(self, target):
        """
        :param target: Vector another point of line
        :return: Vector which is significant to line equation
        """
        from_vec = self.deepcopy()
        target_vec = target.deepcopy()
        x_from, y_from, z_from = from_vec.v
        target_vec.minus(from_vec)
        x_target, y_target, z_target = target_vec.v

