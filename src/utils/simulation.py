__author__ = "Petr Kohout <xkohou14@stud.fit.vutbr.cz>"
__date__ = "$29.8.2020 15:42:10$"

from debug.logger import Loggable
from debug.iniLoader import IniLoader
from utils.pool import Grid
from generator.generator import Generator
from objects.object import Object
from visualization.data_picker import DataPicker


class SimulationManager:

    manager = None

    def __init__(self):
        if not SimulationManager.manager:
            raise EnvironmentError("SimulationManager is not set, please run somewhere SimulationManager.init_manager "
                                   "before you work with that")

    @staticmethod
    def init_manager(INI_FILE):
        if not SimulationManager.manager:
            SimulationManager.manager = SimulationManager.__SimulationManager(INI_FILE)

    class __SimulationManager(Loggable):
        def __init__(self, INI_FILE):
            super().__init__()

            self.ini = INI_FILE + "." + "environment."

            self.time_step = int(IniLoader.load(self.ini + "time_step"))
            self.simulation_finish_time = int(IniLoader.load(self.ini + "simulation_time")) * 1000
            self.simulation_time = 0

            Grid.initPool(INI_FILE)
            self.generators: [Generator] = []
            self.objects: [Object] = []

            self.picker = DataPicker(INI_FILE)

            self.logger.log('created', showInConsole=True)

        def register_generator(self, g: Generator):
            self.generators.append(g)
            self.logger.log('Generator registered', showInConsole=True)

        def register_object(self, o: Object):
            self.objects.append(o)
            self.logger.log('Object '+str(o.id)+' registered', showInConsole=False)

        def run(self):
            self.logger.log('Simulation begins', showInConsole=True)

            while self.simulation_time < self.simulation_finish_time:
                self.logger.log('Simulation time ' + str(self.simulation_time / 1000) + " s", showInConsole=True)
                for i, generator in enumerate(self.generators):
                    elements: [Object] = generator.generate(self.time_step)
                    for i_object, obj in enumerate(elements):
                        self.register_object(obj)
                self.logger.log(Grid().pool, showInConsole=True)
                self.picker.reset()
                self.picker.set_time(self.simulation_time)
                for i_object, obj in enumerate(self.objects):
                    obj.move()
                    self.picker.add(obj.json_str())
                self.picker.logger.log(self.picker.json_str())
                self.picker.store()
                self.simulation_time += self.time_step
            del self.picker
            self.logger.log('Simulation ends', showInConsole=True)
