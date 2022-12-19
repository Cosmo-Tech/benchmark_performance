"""Checkers functions for validations"""
import sys
import os
import shutil
import yaml
from yaml.loader import SafeLoader
from cosmotech_api import ApiClient
from azure.identity import ClientSecretCredential
from utils.configuration import get_configuration
from utils.organization import check_organization_by_id
from utils.workspaces import check_workspace_by_id
from utils.solutions import check_solution_by_id
from utils.connectors import check_connector_by_id
from utils.logger import Logger
sys.dont_write_bytecode=True

logger = Logger.__call__()

class Env():
    """Class to convert dict to object"""
    id = ""
    url= ""
    connector_type: ""
    connector_url: ""
    run_template= ""
    path_input = ""
    compute_size = ""
    name = ""
    type = ""
    name_file_storage = ""
    size = 0
    cosmo_test = {}
    azure = {}
    scenarios = {}
    connector = {}
    dataset = {}
    organization = {}
    workspace = {}
    solution = {}
    def __init__(self, env_dict):
        for key in env_dict:
            setattr(self, key, env_dict[key])


class Services:
    """Build services class injected to all script"""
    def __init__(
        self,
        api_client,
        organization,
        workspace,
        solution,
        connector,
        paths
    ):
        self.api_client = api_client
        self.organization = organization
        self.workspace = workspace
        self.solution = solution
        self.connector = Env({
            'id': connector.get('id'),
            'type': connector.get('type'),
            'name': connector.get('name'),
            'url': connector.get('url'),
        })
        self.paths = Env({
            'data': paths.get('data'),
            'logs': paths.get('logs'),
            'summary': paths.get('summary')
        })

async def verification(parameter_list: list):
    """Verification de key in list generic"""
    for item in parameter_list[0]:
        if item in parameter_list[1]:
            continue
        await logger.logger(f"There is no '{item}' key in cosmotest.config file")
        await logger.logger(f"Please use these keys: {parameter_list[1]}")
        return [False for item in range(3)]

    for item in parameter_list[1]:
        if item in parameter_list[0]:
            continue
        await logger.logger(f"There is no '{item}' key cosmotest.config file")
        await logger.logger(f"Please use these keys: {parameter_list[1]}")
        return [False for item in range(3)]
    return [True for item in range(3)]


async def check_root_keys(env, env_object):
    """check key of root config file"""
    list_root_keys = ['azure', 'cosmo_test']
    response = await verification([list(env.keys()), list_root_keys])
    if all(response):
        azure = env_object.azure
        cosmo = env_object.cosmo_test
        return (azure, cosmo, True)
    return (None, None, None, False)


async def check_azure_keys(azure):
    """check azure keys in config file"""
    list_azure_keys = [
        'tenant_id',
        'client_id',
        'client_secret',
        'cosmo_api_scope',
        'cosmo_api_host'
    ]

    if not azure:
        await logger.logger(f'please add keys in azure section: {list_azure_keys}')
        sys.exit(1)

    response = await verification([azure, list_azure_keys])
    if all(response):
        return (Env(azure), True)
    return (None, False)

async def check_cosmo_keys(cosmo):
    """check cosmo keys in config file"""
    list_cosmo_keys = [
        'organization',
        'workspace',
        'solution',
        'connector',
        'name_file_storage',
        'scenarios'
    ]

    if not cosmo:
        await logger.logger(f'please add keys in cosmo_test section: {list_cosmo_keys}')
        sys.exit(1)

    response = await verification([cosmo, list_cosmo_keys])
    if all(response):
        return (Env(cosmo), True)
    return (None, False)

async def check_cosmo_organization_keys(organization):
    """check organization keys on cosmo_test section config file"""
    list_keys = ['id', 'name']

    if not organization:
        await logger.logger(f'please add keys in {organization} section: {list_keys}')
        sys.exit(1)

    response = await verification([organization, list_keys])
    if all(response):
        return (Env(organization), True)
    return (None, False)


async def check_cosmo_workspace_keys(workspace):
    """check workspace keys on cosmo_test section config file"""
    list_keys = ['id', 'name']

    if not workspace:
        await logger.logger(f'please add keys in workspace section: {list_keys}')
        sys.exit(1)

    response = await verification([workspace, list_keys])
    if all(response):
        return (Env(workspace), True)
    return (None, False)


async def check_cosmo_solution_keys(solution):
    """check solution keys on cosmo_test section config file"""
    list_keys = ['id', 'name', 'version']

    if not solution:
        await logger.logger(f'please add keys in solution section: {list_keys}')
        sys.exit(1)

    response = await verification([solution, list_keys])
    if all(response):
        return (Env(solution), True)
    return (None, False)

async def check_cosmo_scenarios_keys(item):
    """check scenarios keys on cosmo_test config file"""
    list_keys = ['name', 'size', 'compute_size', 'dataset']

    if not item:
        await logger.logger(f'please add a list of scenario in scenarios section: {list_keys}')
        sys.exit(1)

    response = await verification([item, list_keys])
    if all(response):
        return (Env(item), True)
    return (None, False)

async def check_connector_keys(connector):
    """check connector keys on cosmo_test section config file"""
    list_keys = ['id', 'name', 'url']

    if not connector:
        await logger.logger(f'please add keys in connector section:  {list_keys}')
        sys.exit(1)

    response = await verification([connector, list_keys])
    if all(response):
        return (Env(connector), True)
    return (None, False)


async def check_dataset_keys(dataset):
    """check dataset keys on cosmo_test section config file"""
    list_keys = ['name','path_input']
    if not dataset:
        await logger.logger(f'please add keys in dataset section: {list_keys}')
        sys.exit(1)
    response = await verification([dataset, list_keys])
    if all(response):
        return (Env(dataset), True)
    return (None, False)


async def verification_path_exists(path_data, dataset: object):
    """verificator if scenario path exist"""
    if not dataset.path_input:
        await logger.logger(f'The path input of dataset section is empty ex: {path_data}/scenario_a')
        sys.exit(1)
    input_bool = os.path.isdir(f'{path_data}/{dataset.path_input}')
    if not input_bool:
        await logger.logger(f"The path '{path_data}/{dataset.path_input}' not exist")
    return all([input_bool])

async def verification_keys_exists(
        api_client: object,
        organization: object,
        workspace: object,
        solution: object
    ):
    """verificator if keys on azure section exist and there are not empty"""
    if not organization.id:
        await logger.logger('the key id on organization section is empty')
        sys.exit(1)
    organization_bool = await check_organization_by_id(api_client, organization.id)

    if not workspace.id:
        await logger.logger('the key id on workspace section is empty')
        sys.exit(1)
    workspace_bool = await check_workspace_by_id(api_client, organization.id, workspace.id)

    if not solution.id:
        await logger.logger('the key id on solution section is empty')
        sys.exit(1)

    solution_bool = await check_solution_by_id(api_client, organization.id, solution.id)
    return all([organization_bool, workspace_bool, solution_bool])

async def check_connector_exists(api_client: object, connector: object):
    """check if connector key exist and is not empty"""
    if not connector.id:
        await logger.logger('connector id key is empty')
        sys.exit(1)
    return await check_connector_by_id(api_client, connector.id)

async def read_config_file(home) -> dict:
    """.env"""
    cosmotest = os.path.join(home, 'cosmotest.config.yml')
    if os.path.isfile(cosmotest):
        with open(cosmotest, "r", encoding="UTF-8") as config_file:
            data = yaml.load(config_file, Loader=SafeLoader)
            return data
    await logger.logger("No config file: cosmotest.config.yml, please create it before run the test script")
    sys.exit(1)

async def get_api_client(azure: object):
    """get api client cosmotech"""
    dictionary = {
        'tenant_id': azure.tenant_id,
        'client_id':azure.client_id,
        'client_secret': azure.client_secret,
        'cosmo_api_host': azure.cosmo_api_host,
        'cosmo_api_scope': azure.cosmo_api_scope
    }
    for item in enumerate(dictionary):
        if not dictionary.get(item[1]):
            await logger.logger(f'the key : {item[1]} of azure section is empty')
            sys.exit(1)

    credential = ClientSecretCredential(azure.tenant_id, azure.client_id, azure.client_secret)
    token = credential.get_token(azure.cosmo_api_scope).token
    configuration = get_configuration(azure.cosmo_api_host, token)
    return ApiClient(configuration)

async def check_scenario_structure(path_data, cosmo: object):
    """check scenarios structure on config file"""
    for item in cosmo.scenarios:
        check_type = cosmo.scenarios[f"{item}"]
        if isinstance(check_type, str):
            await logger.logger(f"the item {item}: {check_type} is not permited in 'scenarios' section")
            sys.exit(1)

        scenario = Env(cosmo.scenarios[f"{item}"])

        # check scenario keys
        scenario, check_ok = await check_cosmo_scenarios_keys(cosmo.scenarios[f"{item}"])
        if not check_ok:
            sys.exit(1)

        # check dataset keys
        dataset, check_ok = await check_dataset_keys(scenario.dataset)
        if not check_ok:
            sys.exit(1)

        # verification if path exist
        path_exists = await verification_path_exists(path_data, dataset)
        if not path_exists:
            sys.exit(1)

    return True

async def check_all_keys_in_config_file(env, env_object: object):
    """check all keys in config file entry"""
    return_ok = True

    # root
    azure, cosmo, check_ok = await check_root_keys(env, env_object)
    if not check_ok:
        sys.exit(1)

    ## azure key
    azure, check_ok = await check_azure_keys(azure)
    if not check_ok:
        sys.exit(1)

    ## cosmo key
    cosmo, check_ok = await check_cosmo_keys(cosmo)
    if not check_ok:
        sys.exit(1)

    # organization key
    organization, check_ok = await check_cosmo_organization_keys(cosmo.organization)
    if not check_ok:
        sys.exit(1)

    # workspace key
    workspace, check_ok = await check_cosmo_workspace_keys(cosmo.workspace)
    if not check_ok:
        sys.exit(1)

    # solution key
    solution, check_ok = await check_cosmo_solution_keys(cosmo.solution)
    if not check_ok:
        sys.exit(1)

    # check connector keys
    connector, check_ok = await check_connector_keys(cosmo.connector)
    if not check_ok:
        sys.exit(1)

    #check connector exist
    with await get_api_client(azure) as api_client:
        connector_type, check_ok = await check_connector_exists(api_client, connector)
        if not check_ok:
            sys.exit(1)

    if not cosmo.scenarios:
        await logger.logger("No scenarios structure in config file yml.")
        sys.exit(1)

    if return_ok:
        return (azure, cosmo, organization, workspace, solution, connector, connector_type, True)
    sys.exit(1)

def clean_up_data_folder(path_data, path_logs, path_summary):
    """clean up script folders to run correctly"""
    if os.path.isdir(path_data):
        shutil.rmtree(path_data)

    if os.path.isdir(path_logs):
        shutil.rmtree(path_logs)
    os.mkdir(path_logs)

    if os.path.isdir(path_summary):
        shutil.rmtree(path_summary)
    os.mkdir(path_summary)
