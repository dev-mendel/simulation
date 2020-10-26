__author__ = "Petr Kohout <xkohou14@stud.fit.vutbr.cz>"
__date__ = "$30.9.2020 20:29:10$"

from debug.logger import Loggable, Logger
from debug.iniLoader import IniLoader
from shutil import copyfile
import os

class DataPicker(Loggable):

    def __init__(self, INI_FILE):
        super().__init__()

        self.time = 0
        self.data = []
        self.storage = open(Logger.rootPath + IniLoader.load(INI_FILE + '.storage.dir') + IniLoader.load(INI_FILE + '.data-picker.file'), "w")
        self.storage.write('{'
                           '"machine": {'
                                '"x": ' + IniLoader.load(INI_FILE + '.machine.size_x') +
                                ',"y": ' + IniLoader.load(INI_FILE + '.machine.size_y') +
                                ',"z": ' + IniLoader.load(INI_FILE + '.machine.size_z') +
                                ',"entry": {'
                                    '"x": ' + IniLoader.load(INI_FILE + '.machine.entry_x') +
                                    ',"y": ' + IniLoader.load(INI_FILE + '.machine.entry_y') +
                                '},' 
                                '"exit": {'
                                    '"x": ' + IniLoader.load(INI_FILE + '.machine.exit_x') +
                                    ',"y": ' + IniLoader.load(INI_FILE + '.machine.exit_y') +
                                '}' 
                           '},'
                            '"data": [')
        self.ini = INI_FILE

    def __del__(self):
        # close file but finish json object
        self.storage.write("]}")
        self.storage.close()
        if int(IniLoader.load(self.ini + '.data-picker.parse')):
            self.logger.log("Parsing nice json ;) ", showInConsole=True)
            self.parse_file()

    def parse_file(self):
        """just for beautiful json :) """
        swap = open(
            Logger.rootPath + IniLoader.load(self.ini + '.storage.dir') + IniLoader.load(self.ini + '.data-picker.file') + ".swap", "w")
        tabs = 0

        with open(Logger.rootPath + IniLoader.load(self.ini + '.storage.dir') + IniLoader.load(self.ini + '.data-picker.file'), "r") as f:
            while True:
                c = f.read(1)
                tabs_pass = ""
                if not c:
                    break
                elif c == '{':
                    tabs += 1
                    for i in range(tabs):
                        tabs_pass += '\t'
                    swap.write('{\n' + tabs_pass)
                elif c == ',':
                    for i in range(tabs):
                        tabs_pass += '\t'
                    swap.write(',\n' + tabs_pass)
                elif c == '}':
                    tabs -= 1
                    for i in range(tabs):
                        tabs_pass += '\t'
                    swap.write('\n' + tabs_pass + '}')
                else:
                    swap.write(c)
        swap.close()

        copyfile(
            Logger.rootPath + IniLoader.load(self.ini + '.storage.dir') + IniLoader.load(self.ini + '.data-picker.file') + ".swap",
            Logger.rootPath + IniLoader.load(self.ini + '.storage.dir') + IniLoader.load(self.ini + '.data-picker.file')
        )
        os.remove(Logger.rootPath + IniLoader.load(self.ini + '.storage.dir') + IniLoader.load(self.ini + '.data-picker.file') + ".swap")

    def store(self):
        """store to json file"""
        if self.time == 0:
            self.storage.write(self.json_str())
        else:  # it is array of objects so if it is not first make ,
            self.storage.write("," + self.json_str())

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
