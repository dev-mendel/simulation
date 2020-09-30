__author__ = "Petr Kohout <xkohou14@stud.fit.vutbr.cz>"
__date__ = "$30.9.2020 20:29:10$"

from debug.logger import Loggable

class DataPicker(Loggable):

    def __init__(self):
        super().__init__()

        self.time = 0
        self.data = []

    def reset(self):
        self.data = []

    def set_time(self, time):
        """Sets time of simulation"""
        self.time = time

    def add(self, item):
        self.data.append(item)

    def json_str_arr_data(self):
        value = "["
        for i, el in enumerate(self.data):
            value += el
            if i+1 != len(self.data):
                value += ","
        value += "]"

        return value

    def json_str(self):
        return '{ "time": ' + str(self.time) + ',' \
                    '"values": ' + self.json_str_arr_data() + \
               '}'
