import sys
import os
import glob
from utils.constants import DATA_FOLDER, LOGS_FOLDER, INPUT_FOLDER, SUMMARY_FOLDER
from utils.singleton import SingletonType

class Path(object, metaclass=SingletonType):
    HOME = ""
    DATA = ""
    LOGS = ""
    SUMMARY = ""
    INPUT = ""
    zip_file = ""
    def __set_path__(self, HOME):
        self.HOME = HOME
        self.DATA = os.path.join(HOME, DATA_FOLDER)
        self.LOGS = os.path.join(HOME, LOGS_FOLDER)
        self.SUMMARY = os.path.join(HOME, SUMMARY_FOLDER)
        self.INPUT = os.path.join(HOME, INPUT_FOLDER)

        self.zip_file = glob.glob(os.path.join(f"{self.INPUT}","*.zip"))
        self.zip_file = self.zip_file[0] if len(self.zip_file) > 0 else None
        if self.zip_file is None:
          print("no scenarios zip file in input folder")
          sys.exit(1)
        self.zip_file = os.path.basename(self.zip_file)