import os
import yaml
from yaml.loader import SafeLoader
from utils.run_exit import run_exit

from utils.path import Path
PATH = Path.__call__()

from utils.logger import Logger
LOGGER = Logger.__call__()

async def read_config_file():
    cosmotest = os.path.join(PATH.HOME, 'cosmotest.config.yml')
    if os.path.isfile(cosmotest):
        with open(cosmotest, "r", encoding="UTF-8") as config_file:
            data = yaml.load(config_file, Loader=SafeLoader)
            if not data:
                await LOGGER.logger("Please add configuration in config file.")
                await run_exit(LOGGER)
            return data
    await LOGGER.logger("No config file: cosmotest.config.yml, please create it before run the test script")
    await run_exit(LOGGER)