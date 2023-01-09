import os
from utils.run_exit import run_exit

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.path import Path
PATH = Path.__call__()

from utils.services import Services
SERVICES = Services.__call__()

async def check_structure_data_folder():
  folder = os.path.join(PATH.DATA, "scenario")
  if os.path.isdir(folder):
    if not len(os.listdir(folder)):
      await LOGGER.logger(f" {os.path.basename(folder)} folder is empty")
      await run_exit(LOGGER)
