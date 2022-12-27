import sys
import os
import shutil
from utils.configuration import get_configuration
from utils.organization import check_organization_by_id
from utils.workspaces import check_workspace_by_id
from utils.solutions import check_solution_by_id
from utils.connectors import check_connector_by_id
from utils.run_exit import run_exit

from utils.path import Path
PATH = Path.__call__()

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.services import Services
SERVICES = Services.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()

async def verification(parameter_list: list):
    for item in parameter_list[0]:
        if item in parameter_list[1]:
            continue
        await LOGGER.logger(f"There is no '{item}' key in cosmotest.config file")
        await LOGGER.logger(f"Please use these keys: {parameter_list[1]}")
        return [False for item in range(3)]

    for item in parameter_list[1]:
        if item in parameter_list[0]:
            continue
        await LOGGER.logger(f"There is no '{item}' key cosmotest.config file")
        await LOGGER.logger(f"Please use these keys: {parameter_list[1]}")
        return [False for item in range(3)]
    return [True for item in range(3)]


async def check_root_keys(env_object):
    list_root_keys = ['azure', 'cosmo']
    response = await verification([list(env_object.keys()), list_root_keys])
    if all(response):
        return (env_object.get('azure'), env_object.get('cosmo'))
    await run_exit(LOGGER)


async def check_azure_keys(azure):
    list_azure_keys = [
        'tenant_id',
        'client_id',
        'client_secret',
        'cosmo_api_scope',
        'cosmo_api_host'
    ]

    if not azure:
        await LOGGER.logger(f'please add keys in azure section: {list_azure_keys}')
        await run_exit(LOGGER)

    response = await verification([azure, list_azure_keys])
    if all(response):
        return azure
    await run_exit(LOGGER)

async def check_cosmo_keys(cosmo):
    list_cosmo_keys = [
        'organization',
        'workspace',
        'solution',
        'connector',
        'name_file_storage',
        'scenarios'
    ]

    if not cosmo:
        await LOGGER.logger(f'please add keys in cosmo_test section: {list_cosmo_keys}')
        await run_exit(LOGGER)

    response = await verification([cosmo, list_cosmo_keys])
    if all(response):
        return cosmo
    await run_exit(LOGGER)

async def check_cosmo_organization_keys(organization):
    list_keys = ['id', 'name']

    if not organization:
        await LOGGER.logger(f'please add keys in {organization} section: {list_keys}')
        await run_exit(LOGGER)

    response = await verification([organization, list_keys])
    if all(response):
        return organization
    await run_exit(LOGGER)


async def check_cosmo_workspace_keys(workspace):
    list_keys = ['id', 'name']

    if not workspace:
        await LOGGER.logger(f'please add keys in workspace section: {list_keys}')
        await run_exit(LOGGER)

    response = await verification([workspace, list_keys])
    if all(response):
        return workspace
    await run_exit(LOGGER)


async def check_cosmo_solution_keys(solution):
    list_keys = ['id', 'name', 'version']

    if not solution:
        await LOGGER.logger(f'please add keys in solution section: {list_keys}')
        await run_exit(LOGGER)

    response = await verification([solution, list_keys])
    if all(response):
        return solution
    await run_exit(LOGGER)

async def check_cosmo_scenarios_keys(item):
    list_keys = ['name', 'size', 'compute_size', 'dataset']

    if not item:
        await LOGGER.logger(f'please add a list of scenario in scenarios section: {list_keys}')
        await run_exit(LOGGER)

    response = await verification([item, list_keys])
    if all(response):
        return item
    await run_exit(LOGGER)

async def check_connector_keys(connector):
    list_keys = ['id', 'name', 'url']

    if not connector:
        await LOGGER.logger(f'please add keys in connector section:  {list_keys}')
        await run_exit(LOGGER)

    response = await verification([connector, list_keys])
    if all(response):
        return connector
    await run_exit(LOGGER)


async def check_dataset_keys(dataset):
    list_keys = ['name','path_input']
    if not dataset:
        await LOGGER.logger(f'please add keys in dataset section: {list_keys}')
        await run_exit(LOGGER)
    response = await verification([dataset, list_keys])
    if all(response):
        return dataset
    await run_exit(LOGGER)


async def verification_path_exists(dataset):
    if not dataset.get('path_input'):
        await LOGGER.logger(f'The path input of dataset section is empty ex: {PATH.DATA}/scenario_a')
        await run_exit(LOGGER)
    input_bool = os.path.isdir(f"{PATH.DATA}/{dataset.get('path_input')}")
    if not input_bool:
        await LOGGER.logger(f"The path '{PATH.DATA}/{dataset.get('path_input')}' not exist")
    return all([input_bool])

async def verification_keys_exists():
    if not SERVICES.organization.get('id'):
        await LOGGER.logger('the key id on organization section is empty')
        await run_exit(LOGGER)
    organization_bool = await check_organization_by_id()

    if not SERVICES.workspace.get('id'):
        await LOGGER.logger('the key id on workspace section is empty')
        await run_exit(LOGGER)
    workspace_bool = await check_workspace_by_id()

    if not SERVICES.solution.get('id'):
        await LOGGER.logger('the key id on solution section is empty')
        await run_exit(LOGGER)

    solution_bool = await check_solution_by_id()
    return all([organization_bool, workspace_bool, solution_bool])

async def check_connector_exists(connector: dict):
    if not connector.get('id'):
        await LOGGER.logger('connector id key is empty')
        await run_exit(LOGGER)
    return await check_connector_by_id(connector.get('id'))

async def check_scenario_structure():
    cosmo = SERVICES.cosmo.get('scenarios')
    for k,item in enumerate(cosmo):
        check_type = cosmo[k]
        if isinstance(check_type, str):
            await LOGGER.logger(f"the item {item}: {check_type} is not permited in 'scenarios' section")
            await run_exit(LOGGER)

        scenario = cosmo[k]

        # check scenario keys
        scenario = await check_cosmo_scenarios_keys(cosmo[k])

        # check dataset keys
        dataset = await check_dataset_keys(scenario.get('dataset'))

        # verification if path exist
        path_exists = await verification_path_exists(dataset)
        if not path_exists:
            await run_exit(LOGGER)

async def check_all_keys_in_config_file(env_object):
    # root
    azure, cosmo = await check_root_keys(env_object)
    ## azure key
    azure = await check_azure_keys(azure)
    ## cosmo key
    cosmo = await check_cosmo_keys(cosmo)
    # organization key
    organization = await check_cosmo_organization_keys(cosmo.get('organization'))
    # workspace key
    workspace = await check_cosmo_workspace_keys(cosmo.get('workspace'))
    # solution key
    solution = await check_cosmo_solution_keys(cosmo.get('solution'))
    # check connector keys
    connector = await check_connector_keys(cosmo.get('connector'))

    SERVICES.__set__(azure, cosmo, organization, workspace, solution, connector)
    #check connector exist
    connector_type = await check_connector_exists(connector)
    SERVICES.__set__(azure, cosmo, organization, workspace, solution, connector, connector_type)

    if not cosmo.get('scenarios'):
        await LOGGER.logger("No scenarios structure in config file yml.")
        await run_exit(LOGGER)

def clean_up_data_folder():
    if os.path.isdir(PATH.DATA):
        shutil.rmtree(PATH.DATA)

    if os.path.isdir(PATH.LOGS):
        shutil.rmtree(PATH.LOGS)
    os.mkdir(PATH.LOGS)

    if os.path.isdir(PATH.SUMMARY):
        shutil.rmtree(PATH.SUMMARY)
    os.mkdir(PATH.SUMMARY)
