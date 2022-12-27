import os
from utils.singleton import SingletonType

class Path(object, metaclass=SingletonType):
    HOME = ""
    DATA = ""
    LOGS = ""
    SUMMARY = ""
    PARAMETER = ""
    def __set_path__(self, HOME):
        self.HOME = HOME
        self.DATA = os.path.join(HOME, "data")
        self.LOGS = os.path.join(HOME, "logs")
        self.SUMMARY = os.path.join(HOME, "summary")
        self.PARAMETER = os.path.join(HOME, "parameter")