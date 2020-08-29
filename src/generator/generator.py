__author__ = "Petr Kohout <xkohou14@stud.fit.vutbr.cz>"
__date__ = "$29.8.2020 10:50:10$"

from abc import abstractmethod

from debug.logger import Loggable
#from objects.object import Object


class Generator(Loggable):

    def __init__(self, INI_FILE, INI_LOADER_NAME):
        super().__init__()

        self.ini = INI_FILE + "." + INI_LOADER_NAME + "."

    @abstractmethod
    def generate(self, time_step):
        """
        :param time_step: int
        :return: [Object]
        """
        pass
