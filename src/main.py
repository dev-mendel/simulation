import sys

from utils.simulation import SimulationManager
from generator.machine_entry import MachineEntry


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Too few arguments, please specify your ini file")
    else:
        ini_file = sys.argv[1]
        SimulationManager.init_manager(ini_file)
        SimulationManager().manager.register_generator(MachineEntry(ini_file))
        SimulationManager().manager.run()