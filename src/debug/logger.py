# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Pavel Kohout <xkohou15@stud.fit.vutbr.cz>"
__date__ = "$5.6.2018 22:43:10$"

import configparser
import datetime
import os

class Logger:
    """
    Logging data into log files created with names of classes
    Structure:
    ######## CLASS NAME 
    Event: Description
    DD/MM/YY HH:MM:SS
    """
    
    """Variable for name of calling class"""
    className = ""
    """Variable for log file"""
    logFile = ""
    """Variable for log file for all logs"""
    allLogFile = ""
    """Enable logging in general file"""
    enableGeneral = True
    """Root folder path"""
    rootPath = "../"
    """Configuration folder path"""
    configPath = rootPath + "config/"
    
    def __init__(self, classRef):
        """
        Creates logger for specific class
        """
        config = configparser.ConfigParser()
        config.read(Logger.rootPath + 'config/template.ini')
        self.className = str(classRef.__class__.__name__)
        """appends log file"""
        self.logFile = open(Logger.rootPath + config['logger']['dir_path'] + self.className + ".log", "a")
        """appends log file for all logs"""
        self.allLogFile = open(Logger.rootPath + config['logger']['dir_path'] + config['logger']['general'] + ".log", "a")
        
        #creates logs dir
        if not os.path.exists(Logger.rootPath + config['logger']['dir_path']):
            os.makedirs(Logger.rootPath + config['logger']['dir_path'])

    def __del__(self):
        self.logFile.close()
        self.allLogFile.close()
        
    def log(self, description, showInConsole=False):
        """logs event"""
        self.logFile.write("######## " + self.className + "\n")
        self.logFile.write("Event: " + str(description) + "\n")
        self.logFile.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n\n")
        if self.enableGeneral:
            self.allLogFile.write("######## " + self.className + "\n")
            self.allLogFile.write("Event: " + str(description) + "\n")
            self.allLogFile.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n\n")

        if showInConsole:
            print("######## " + self.className + "\n", flush=True)
            print("Event: " + str(description) + "\n", flush=True)
            print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n\n", flush=True)
      
    @staticmethod
    def clean():
        """Clean all logs files"""
        config = configparser.ConfigParser()
        config.read(Logger.configPath + 'debug.ini')
        print("Current path: " + str(os.path.abspath('.')))
        
        #creates logs dir
        if not os.path.exists(Logger.rootPath + config['logger']['dir_path']):
            os.makedirs(Logger.rootPath + config['logger']['dir_path'])
        
        folder = Logger.rootPath + config['logger']['dir_path']
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                logger = Logger(Logger())
                logger.log("Exception during cleaning: " + str(e))


class Loggable:

    def __init__(self):
        #print("Creating logger " + self.__class__.__name__)
        self.logger = Logger(self)
