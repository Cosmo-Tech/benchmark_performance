""".env"""
import os
import glob
import sys
# import time
from checks_functions.validation_config_file import Env
from checks_functions.validation_config_file import check_scenario_structure
from checks_functions.validation_config_file import read_config_file, get_api_client
from checks_functions.validation_config_file import check_all_keys_in_config_file
from checks_functions.validation_config_file import verification_keys_exists
from dataset.download_files_from_perf_account import download_files

def get_scenarios() -> dict:
    """retrieve all scenarios from config file"""
    print('Checking configuration...')

    env = read_config_file()
    if not env:
        print("Please add configuration in config file.")
        sys.exit(1)
    env_object = Env(env)

    azure, cosmo, organization, workspace, solution, connector, connector_type, check_ok = check_all_keys_in_config_file(env, env_object)
    if not check_ok:
        sys.exit(1)

    # verification if keys values exist
    with get_api_client(azure) as api_client:
        environment_cosmo_is_ok = verification_keys_exists(
            api_client,
            organization,
            workspace,
            solution
        )

    if environment_cosmo_is_ok:
        if not os.path.isdir("./data"):
            os.mkdir('./data')
            data_directory = os.listdir("./data")
            if len(data_directory) == 0:
                download = download_and_unzip_dataset_test_from_storage(cosmo.name_file_storage)
                if not download:
                    sys.exit(1)

        check_ok = check_scenario_structure(cosmo)
        if not check_ok:
            sys.exit(1)

        # check scenario items
        scenarios_list = [cosmo.scenarios[f"{item}"] for item in cosmo.scenarios]
        check_scenario_item(scenarios_list)

        print(f"{len(cosmo.scenarios.keys())} scenario(s)... configuration OK")
        return (api_client, organization.id, solution.id, workspace.id, cosmo.name_file_storage, connector, connector_type, scenarios_list)
    sys.exit(1)

def download_and_unzip_dataset_test_from_storage(name_file_storage: str):
    """download zip file and unzip it"""
    return download_files(name_file_storage)

def check_scenario_item(scenarios_list: list):
    """check scenario items config file"""
    for item in scenarios_list:
        scenario_object = Env(item)
        dictionary_scenario = {
            'name': scenario_object.name,
            'size': scenario_object.size,
            'compute_size': scenario_object.compute_size,
            'dataset': scenario_object.dataset
        }

        for item in enumerate(dictionary_scenario):
            if item[1] == 'compute_size':
                if not dictionary_scenario.get(item[1]) in ["highcpu", "basicpool"]:
                    print("check your compute_size value: 'basicpool' or 'highcpu' (case sensitive)")
                    sys.exit(1)

            if not dictionary_scenario.get(item[1]):
                print(f'the key : {item[1]} on scenario section is empty')
                sys.exit(1)

        # check dataset item
        dataset_object = Env(scenario_object.dataset)
        dictionary_dataset = {
            "name": dataset_object.name,
            "path_input": dataset_object.path_input
        }
        for item in enumerate(dictionary_dataset):
            if not dictionary_dataset.get(item[1]):
                print(f'the key : {item[1]} on dataset section is empty')
                sys.exit(1)

        scenario_folder = os.listdir(f'./data/{dataset_object.path_input}')
        if len(scenario_folder) == 0:
            print('folder empty', dataset_object.path_input, "no dataset folder")
            sys.exit(1)

        dataset_dir_exist = os.path.isdir(os.path.join(f'./data/{dataset_object.path_input}','dataset'))
        if not dataset_dir_exist:
            print('not dataset folder in scenario', dataset_object.path_input)
            sys.exit(1)

        json_file_name = glob.glob(os.path.join(f"./data/{dataset_object.path_input}/","*.json"))
        if len(json_file_name) == 0:
            print('No json scenario file in:', dataset_object.path_input)
            sys.exit(1)

        # check is dataset folder is empty
        files_in_dataset_folder = glob.glob(os.path.join(f"./data/{dataset_object.path_input}/dataset","*.*"))
        if len(files_in_dataset_folder) == 0:
            print("folder", f'{dataset_object.path_input}/dataset', "is empty")
            sys.exit(1)
