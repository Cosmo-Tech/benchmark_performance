import os
import shutil

from utils.path import Path
PATH = Path.__call__()

def clean_up_data_folder():
    if os.path.isdir(PATH.DATA):
        shutil.rmtree(PATH.DATA)
    os.mkdir(PATH.DATA)

    if os.path.isdir(PATH.LOGS):
        shutil.rmtree(PATH.LOGS)
    os.mkdir(PATH.LOGS)

    if os.path.isdir(PATH.SUMMARY):
        shutil.rmtree(PATH.SUMMARY)
    os.mkdir(PATH.SUMMARY)

    if not os.path.isdir(PATH.INPUT):
        os.mkdir(PATH.INPUT)