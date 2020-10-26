import sys

from utils.simulation import SimulationManager
from generator.machine_entry import MachineEntry
from generator.machine_exit import MachineExit
from generator.ball_generator import BallGenerator
from debug.iniLoader import IniLoader
from debug.logger import Logger


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Too few arguments, please specify your ini file")
    else:
        ini_file = sys.argv[1]
        if int(IniLoader.load(ini_file + ".logger.clean")):
            Logger.clean()
        SimulationManager.init_manager(ini_file)
        SimulationManager().manager.register_generator(MachineEntry(ini_file))
        SimulationManager().manager.register_generator(MachineExit(ini_file))
        SimulationManager().manager.register_generator(BallGenerator(ini_file))
        SimulationManager().manager.run()
