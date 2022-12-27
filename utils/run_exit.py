import sys

async def run_exit(LOGGER):
    if LOGGER:
        await LOGGER.logger("EXIT")
    sys.exit(1)