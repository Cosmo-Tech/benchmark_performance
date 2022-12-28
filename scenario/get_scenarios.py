""".env"""
import os
from dataset.download_files_from_perf_account import download_files
from dataset.upload_dataset_files_to_perf_account import upload_input_files
from dataset.get_dataset import get_datasets_by_tags
from utils.constants import COMPUTE_SIZE, DATASET, ITEMS_COMPUTE_SIZE, NAME, SCENARIOS, SIZE, TAGS_DATASET, TAGS_DATASET_PERFORMANCE_TEST
from utils.validation_config_file import check_scenario_structure
from utils.read_config_file import read_config_file
from utils.validation_config_file import check_all_keys_in_config_file
from utils.run_exit import run_exit

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.path import Path
PATH = Path.__call__()

from utils.services import Services
SERVICES = Services.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()


async def download_zip_folder():
    if os.path.isdir(PATH.DATA):
        if len(os.listdir(PATH.DATA)) == 0:
            await download_files()

async def upload_zip_file():
    if os.path.isdir(PATH.INPUT):
        if len(os.listdir(PATH.INPUT)) != 0:
            await upload_input_files()

async def get_scenarios():

    env = await read_config_file()

    await check_all_keys_in_config_file(env)

    await upload_zip_file()
    # download input folder
    await download_zip_folder()

    # check scenarios section
    await check_scenario_structure()

    # check scenario items
    scenarios_list = SERVICES.cosmo.get(SCENARIOS)
    await check_scenario_item(scenarios_list)

    await LOGGER.logger(f"{len(SERVICES.cosmo.get(SCENARIOS))} scenario(s)... configuration OK")
    await get_datasets_by_tags(TAGS_DATASET)
    await get_datasets_by_tags(TAGS_DATASET_PERFORMANCE_TEST)
    return scenarios_list

async def check_scenario_item(scenarios_list):
    for scenario_item in scenarios_list:
        dictionary_scenario = {
            NAME: scenario_item.get(NAME),
            SIZE: scenario_item.get(SIZE),
            COMPUTE_SIZE: scenario_item.get(COMPUTE_SIZE),
            DATASET: scenario_item.get(DATASET)
        }
        for item in dictionary_scenario:
            if item == COMPUTE_SIZE:
                if not dictionary_scenario.get(item) in ITEMS_COMPUTE_SIZE:
                    await LOGGER.logger(f"check your compute_size value: {ITEMS_COMPUTE_SIZE} (case sensitive)")
                    await run_exit(LOGGER)

            if not dictionary_scenario.get(item):
                await LOGGER.logger(f'the key : {item} on scenario section is empty')
                await run_exit(LOGGER)
