""".env"""
import os
import glob
from dataset.download_files_from_perf_account import download_files
from utils.validation_config_file import check_scenario_structure
from utils.read_config_file import read_config_file
from utils.validation_config_file import check_all_keys_in_config_file
from utils.validation_config_file import verification_keys_exists
from utils.run_exit import run_exit

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.path import Path
PATH = Path.__call__()

from utils.services import Services
SERVICES = Services.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()

async def get_scenarios():

    env = await read_config_file()
    await check_all_keys_in_config_file(env)

    # verification if keys values exist
    await verification_keys_exists()

    if not os.path.isdir(PATH.DATA):
        os.mkdir(PATH.DATA)
        data_directory = os.listdir(PATH.DATA)
        if len(data_directory) == 0:
            download = await download_and_unzip_dataset_test_from_storage()
            if not download:
                await run_exit(LOGGER)

        await check_scenario_structure()

        # check scenario items
        scenarios_list = SERVICES.cosmo.get('scenarios')
        await check_scenario_item(scenarios_list)

        await LOGGER.logger(f"{len(SERVICES.cosmo.get('scenarios'))} scenario(s)... configuration OK")
        return scenarios_list

async def download_and_unzip_dataset_test_from_storage():
    return await download_files()

async def check_scenario_item(scenarios_list):
    for scenario_item in scenarios_list:
        dictionary_scenario = {
            'name': scenario_item.get('name'),
            'size': scenario_item.get('size'),
            'compute_size': scenario_item.get('compute_size'),
            'dataset': scenario_item.get('dataset')
        }
        for item in dictionary_scenario:
            if item == 'compute_size':
                if not dictionary_scenario.get(item) in ["highcpu", "basic", "memory"]:
                    await LOGGER.logger("check your compute_size value: 'basic', 'highcpu', 'memory' (case sensitive)")
                    await run_exit(LOGGER)

            if not dictionary_scenario.get(item):
                await LOGGER.logger(f'the key : {item} on scenario section is empty')
                await run_exit(LOGGER)

        # check dataset item
        dataset_object = scenario_item.get('dataset')
        path_input = dataset_object.get('path_input')
        dictionary_dataset = {
            "name": dataset_object.get('name'),
            "path_input": dataset_object.get('path_input')
        }
        for item in dictionary_dataset:
            if not dictionary_dataset.get(item):
                await LOGGER.logger(f'the key : {item} on dataset section is empty')
                await run_exit(LOGGER)

        scenario_folder = os.listdir(f'{PATH.DATA}/{path_input}')
        if len(scenario_folder) == 0:
            await LOGGER.logger(f"folder empty {path_input} no dataset folder")
            await run_exit(LOGGER)

        dataset_dir_exist = os.path.isdir(os.path.join(f'{PATH.DATA}/{path_input}','dataset'))
        if not dataset_dir_exist:
            await LOGGER.logger(f"not dataset folder in scenario {path_input}")
            await run_exit(LOGGER)

        json_file_name = glob.glob(os.path.join(f"{PATH.DATA}/{path_input}/","*.json"))
        if len(json_file_name) == 0:
            await LOGGER.logger(f"No json scenario file in: {path_input}")
            await run_exit(LOGGER)

        # check is dataset folder is empty
        files_in_dataset_folder = glob.glob(os.path.join(f"{PATH.DATA}/{path_input}/dataset","*.*"))
        if len(files_in_dataset_folder) == 0:
            await LOGGER.logger(f"folder {path_input}/dataset is empty")
            await run_exit(LOGGER)
