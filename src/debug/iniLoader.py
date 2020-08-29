__author__ = "Petr Kohout <xkohou14@stud.fit.vutbr.cz>"
__date__ = "$23.12.2018 22:43:10$"

import configparser

from .logger import Logger

class IniLoader:
    """
    Loads data from ini file. 
    Path is separated by '.' and first part is name of .ini file
    
    example: db.ini.load
    
    will load from ..config/db.ini
        [ini]
            load = ...
    """
    
    @staticmethod
    def load(path):
        """Loads ini value"""
        logger = Logger(IniLoader())
        logger.enableGeneral = False    
        
        params = path.split(".")
        if (len(params) != 3):
            logger.log("ERROR: Too few parts of path (should have 3 parts): " + path, showInConsole=True)
            return ""
        
        parser = configparser.ConfigParser()
        parser.read(Logger.rootPath + "config/" + params[0] + ".ini")
        value = parser[params[1]][params[2]]
        
        logger.log("From path: " + path + "\n Loaded: " + str(value))
        return value

