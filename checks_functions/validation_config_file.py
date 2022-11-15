""".env"""
import sys
import os
import shutil
import yaml
from yaml.loader import SafeLoader
from cosmotech_api import ApiClient
from azure.identity import ClientSecretCredential
from checks_functions.configuration import get_configuration
from checks_functions.organization import check_organization_by_id
from checks_functions.workspaces import check_workspace_by_id
from checks_functions.solutions import check_solution_by_id
from checks_functions.connectors import check_connector_by_id
sys.dont_write_bytecode=True

class Env():
    """.env"""
    id = ""
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
    """.env"""
    def __init__(
        self,
        api_client,
        organization_id: str,
        workspace_id: str,
        solution_id: str,
        connector_id: str,
    ):
        self.api_client = api_client
        self.organization_id = organization_id
        self.workspace_id = workspace_id
        self.solution_id = solution_id
        self.connector_id = connector_id

def verification(parameter_list: list):
    """.env"""
    for item in parameter_list[0]:
        if item in parameter_list[1]:
            continue
        print(f"There is no '{item}' key in cosmotest.config file")
        print(f"Please use these keys: {parameter_list[1]}")
        return [False for item in range(3)]

    for item in parameter_list[1]:
        if item in parameter_list[0]:
            continue
        print(f"There is no '{item}' key cosmotest.config file")
        print(f"Please use these keys: {parameter_list[1]}")
        return [False for item in range(3)]
    return [True for item in range(3)]


def check_root_keys(env, env_object):
    """.env"""
    list_root_keys = ['azure', 'cosmo_test']
    response = verification([list(env.keys()), list_root_keys])
    if all(response):
        azure = env_object.azure
        cosmo = env_object.cosmo_test
        return (azure, cosmo, True)
    return (None, None, None, False)


def check_azure_keys(azure):
    """.env"""
    list_azure_keys = [
        'tenant_id',
        'client_id',
        'client_secret',
        'cosmo_api_scope',
        'cosmo_api_host'
    ]

    if not azure:
        print('please add keys in azure section: ', list_azure_keys)
        sys.exit(1)

    response = verification([azure, list_azure_keys])
    if all(response):
        return (Env(azure), True)
    return (None, False)

def check_cosmo_keys(cosmo):
    """.env"""
    list_cosmo_keys = [
        'organization',
        'workspace',
        'solution',
        'connector',
        'name_file_storage',
        'scenarios'
    ]

    if not cosmo:
        print('please add keys in cosmo_test section: ', list_cosmo_keys)
        sys.exit(1)

    response = verification([cosmo, list_cosmo_keys])
    if all(response):
        return (Env(cosmo), True)
    return (None, False)

def check_cosmo_organization_keys(organization):
    """.env"""
    list_keys = ['id', 'name']

    if not organization:
        print(f'please add keys in {organization} section: ', list_keys)
        sys.exit(1)

    response = verification([organization, list_keys])
    if all(response):
        return (Env(organization), True)
    return (None, False)


def check_cosmo_workspace_keys(workspace):
    """.env"""
    list_keys = ['id', 'name']

    if not workspace:
        print('please add keys in workspace section: ', list_keys)
        sys.exit(1)

    response = verification([workspace, list_keys])
    if all(response):
        return (Env(workspace), True)
    return (None, False)


def check_cosmo_solution_keys(solution):
    """.env"""
    list_keys = ['id', 'name']

    if not solution:
        print('please add keys in solution section: ', list_keys)
        sys.exit(1)

    response = verification([solution, list_keys])
    if all(response):
        return (Env(solution), True)
    return (None, False)

def check_cosmo_scenarios_keys(item):
    """.env"""
    list_keys = ['name', 'size', 'compute_size', 'dataset']

    if not item:
        print('please add a list of scenario in scenarios section: ', list_keys)
        sys.exit(1)

    response = verification([item, list_keys])
    if all(response):
        return (Env(item), True)
    return (None, False)

def check_connector_keys(connector):
    """.env"""
    list_keys = ['id', 'name']

    if not connector:
        print('please add keys in connector section: ', list_keys)
        sys.exit(1)

    response = verification([connector, list_keys])
    if all(response):
        return (Env(connector), True)
    return (None, False)


def check_dataset_keys(dataset):
    """.env"""
    list_keys = ['name','path_input']
    if not dataset:
        print('please add keys in dataset section: ', list_keys)
        sys.exit(1)
    response = verification([dataset, list_keys])
    if all(response):
        return (Env(dataset), True)
    return (None, False)


def verification_path_exists(dataset: object):
    """.env"""
    if not dataset.path_input:
        print('The path input of dataset section is empty', 'ex: ./data/scenario_a')
        sys.exit(1)
    input_bool = os.path.isdir(f'./data/{dataset.path_input}')
    if not input_bool:
        print(f"The path './data/{dataset.path_input}' not exist")
    return all([input_bool])

def verification_keys_exists(
        api_client: object,
        organization: object,
        workspace: object,
        solution: object
    ):
    """.env"""
    if not organization.id:
        print('the key id on organization section is empty')
        sys.exit(1)
    organization_bool = check_organization_by_id(api_client, organization.id)

    if not workspace.id:
        print('the key id on workspace section is empty')
        sys.exit(1)
    workspace_bool = check_workspace_by_id(api_client, organization.id, workspace.id)

    if not solution.id:
        print('the key id on solution section is empty')
        sys.exit(1)

    solution_bool = check_solution_by_id(api_client, organization.id, solution.id)
    return all([organization_bool, workspace_bool, solution_bool])

def check_connector_exists(api_client: object, connector: object):
    """.env"""
    if not connector.id:
        print('connector id key is empty')
        sys.exit(1)
    return check_connector_by_id(api_client, connector.id)

def read_config_file() -> dict:
    """.env"""
    if os.path.isfile('cosmotest.config.yml'):
        with open('cosmotest.config.yml', "r", encoding="UTF-8") as config_file:
            data = yaml.load(config_file, Loader=SafeLoader)
            return data
    print("No config file: cosmotest.config.yml", "please create it before run the test script")
    sys.exit(1)

def get_api_client(azure: object):
    """.env"""
    dictionary = {
        'tenant_id': azure.tenant_id,
        'client_id':azure.client_id,
        'client_secret': azure.client_secret,
        'cosmo_api_host': azure.cosmo_api_host,
        'cosmo_api_scope': azure.cosmo_api_scope
    }
    for item in enumerate(dictionary):
        if not dictionary.get(item[1]):
            print(f'the key : {item[1]} of azure section is empty')
            sys.exit(1)

    credential = ClientSecretCredential(azure.tenant_id, azure.client_id, azure.client_secret)
    token = credential.get_token(azure.cosmo_api_scope).token
    configuration = get_configuration(azure.cosmo_api_host, token)
    return ApiClient(configuration)

def check_scenario_structure(cosmo: object):
    """.env"""
    for item in cosmo.scenarios:
        check_type = cosmo.scenarios[f"{item}"]
        if isinstance(check_type, str):
            print(f"the item {item}: {check_type} is not permited in 'scenarios' section")
            sys.exit(1)

        scenario = Env(cosmo.scenarios[f"{item}"])

        # check scenario keys
        scenario, check_ok = check_cosmo_scenarios_keys(cosmo.scenarios[f"{item}"])
        if not check_ok:
            sys.exit(1)

        # check dataset keys
        dataset, check_ok = check_dataset_keys(scenario.dataset)
        if not check_ok:
            sys.exit(1)

        # verification if path exist
        path_exists = verification_path_exists(dataset)
        if not path_exists:
            sys.exit(1)


    return True

def check_all_keys_in_config_file(env, env_object: object):
    """.env"""
    return_ok = True

    # root
    azure, cosmo, check_ok = check_root_keys(env, env_object)
    if not check_ok:
        sys.exit(1)

    ## azure key
    azure, check_ok = check_azure_keys(azure)
    if not check_ok:
        sys.exit(1)

    ## cosmo key
    cosmo, check_ok = check_cosmo_keys(cosmo)
    if not check_ok:
        sys.exit(1)

    # organization key
    organization, check_ok = check_cosmo_organization_keys(cosmo.organization)
    if not check_ok:
        sys.exit(1)

    # workspace key
    workspace, check_ok = check_cosmo_workspace_keys(cosmo.workspace)
    if not check_ok:
        sys.exit(1)

    # solution key
    solution, check_ok = check_cosmo_solution_keys(cosmo.solution)
    if not check_ok:
        sys.exit(1)

    # check connector keys
    connector, check_ok = check_connector_keys(cosmo.connector)
    if not check_ok:
        sys.exit(1)

    #check connector exist
    with get_api_client(azure) as api_client:
        check_ok = check_connector_exists(api_client, connector)
        if not check_ok:
            sys.exit(1)

    if not cosmo.scenarios:
        print("No scenarios structure in config file yml.")
        sys.exit(1)

    if return_ok:
        return (azure, cosmo, organization, workspace, solution, connector, True)
    sys.exit(1)

def clean_up_data_folder():
    """.env"""
    if os.path.isdir("./data"):
        shutil.rmtree("./data")

    if os.path.isdir("./logs"):
        shutil.rmtree("./logs")
    os.mkdir("./logs")

    if os.path.isdir("./summary"):
        shutil.rmtree("./summary")
    os.mkdir("./summary")
