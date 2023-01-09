import os
from dataset.download_files_from_perf_account import download_files
from dataset.upload_dataset_files_to_perf_account import upload_input_files
from dataset.get_dataset import get_datasets_by_tags
from utils.constants import COMPUTE_SIZE, DATASET as DATASET_STR
from utils.constants import PATH_INPUT, ITEMS_COMPUTE_SIZE
from utils.constants import NAME, SCENARIOS, SIZE, TAGS_DATASET, TAGS_DATASET_PERFORMANCE_TEST
from utils.validation_config_file import check_scenario_structure
from utils.read_config_file import read_config_file
from utils.validation_config_file import check_all_keys_in_config_file
from utils.run_exit import run_exit
from utils.check_structure_data_folder import check_structure_data_folder

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.path import Path
PATH = Path.__call__()

from utils.services import Services
SERVICES = Services.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()

from utils.datasets import DatasetsList
DATASET = DatasetsList.__call__()


async def download_zip_folder():
    if not os.path.isdir(PATH.DATA):
        await LOGGER.logger("no data folder")
        await run_exit(LOGGER)
    if len(os.listdir(PATH.DATA)) == 0:
        await download_files()
        await check_structure_data_folder()

async def upload_zip_file():
    if not os.path.isdir(PATH.INPUT):
        await LOGGER.logger("no input folder")
        await run_exit(LOGGER)
    if len(os.listdir(PATH.INPUT)) != 0:
        await upload_input_files()
    else:
        await LOGGER.logger("no excel file in input folder")
        await run_exit(LOGGER)

async def get_scenarios():

    env = await read_config_file()

    await check_all_keys_in_config_file(env)

    await upload_zip_file()
    # download input folder
    await download_zip_folder()

    await get_datasets_by_tags(TAGS_DATASET)
    await get_datasets_by_tags(TAGS_DATASET_PERFORMANCE_TEST)
    
    await check_dataset_item()

    # check scenario items
    scenarios_list = SERVICES.cosmo.get(SCENARIOS)
    await check_scenario_item(scenarios_list)
    
    # check scenarios section
    await check_scenario_structure()
    
    await LOGGER.logger(f"{len(SERVICES.cosmo.get(SCENARIOS))} scenario(s)... configuration OK")
    return scenarios_list

async def check_dataset_item():
    for dataset_folder in SERVICES.datasets:
        name = dataset_folder.get(NAME)
        path_input = dataset_folder.get(PATH_INPUT)
        if path_input is None:
            pass
        else:
            if name is None:
                await LOGGER.logger(f"the name of dataset {path_input} is empty")
                await run_exit(LOGGER)

            path_dataset = os.path.join(PATH.DATA, f"dataset/{dataset_folder.get(PATH_INPUT)}")
            if not os.path.isdir(path_dataset):
                await LOGGER.logger(f"the dataset '{os.path.basename(path_dataset)}' does not match with any dataset in data folder")
                await run_exit(LOGGER)

async def check_scenario_item(scenarios_list):
    for scenario_item in scenarios_list:
        # check scenario folder match in config file
        name = scenario_item.get(NAME)
        dataset_name = scenario_item.get(DATASET_STR)
        await check_name_scenario_folder(name)
        await check_dataset_name_exist(name, dataset_name)

        dictionary_scenario = {
            NAME: scenario_item.get(NAME),
            SIZE: scenario_item.get(SIZE),
            COMPUTE_SIZE: scenario_item.get(COMPUTE_SIZE),
            DATASET: scenario_item.get(DATASET_STR)
        }
        for item in dictionary_scenario:
            if item == COMPUTE_SIZE:
                if not dictionary_scenario.get(item) in ITEMS_COMPUTE_SIZE:
                    await LOGGER.logger(f"check your compute_size value: {ITEMS_COMPUTE_SIZE} (case sensitive)")
                    await run_exit(LOGGER)

            if not dictionary_scenario.get(item):
                await LOGGER.logger(f'the key : {item} on scenario section is empty')
                await run_exit(LOGGER)

async def check_name_scenario_folder(name):
    folders = os.listdir(os.path.join(PATH.DATA, "scenario"))
    if name in folders:
        pass
    else:
        await LOGGER.logger(f"scenario '{name}' not exist in data folder")
        await run_exit(LOGGER)

async def check_dataset_name_exist(name, dataset_name):
    if dataset_name is None:
        await LOGGER.logger(f"dataset name is empty in scenario '{name}'")
        await run_exit(LOGGER)

    element = list(filter(lambda d: d.get(NAME).lower() == dataset_name.lower(), DATASET.list))
    exist = element[0] if len(element) > 0 else None
    if exist is None:
        await LOGGER.logger(f"dataset name '{dataset_name}' does not exist")
        await run_exit(LOGGER)
        