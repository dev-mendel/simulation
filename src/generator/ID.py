__author__ = "Petr Kohout <xkohou14@stud.fit.vutbr.cz>"
__date__ = "$29.8.2020 10:50:10$"


class ID:
    """
    Singleton class for generating of unique ids
    """
    generator = None

    def __init__(self):
        if not ID.generator:
            ID.generator = ID.__ID()

    def getID(self):
        ID.generator.id += 1
        return ID.generator.id - 1

    class __ID:
        def __init__(self):
            self.id = 1
