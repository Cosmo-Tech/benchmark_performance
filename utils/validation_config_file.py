import os
from utils.constants import AZURE, AZURE_KEYS, CONNECTOR
from utils.constants import COSMO, COSMO_KEYS, DATASET 
from utils.constants import DATASET_KEYS, ORGANIZATION_ID 
from utils.constants import ROOT_KEYS, SCENARIOS
from utils.constants import SCENARIOS_KEYS, WORKSPACE_ID
from utils.organization import check_organization_by_id
from utils.workspaces import check_workspace_by_id
from utils.solutions import check_solution_by_id
from utils.connectors import get_connectors
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
        await LOGGER.logger(f"there is no '{item}' key in configuration file")
        await LOGGER.logger(f"please use these keys: {parameter_list[1]}")
        await run_exit(LOGGER)

    for item in parameter_list[1]:
        if item in parameter_list[0]:
            continue
        await LOGGER.logger(f"there is no '{item}' key in configuration file")
        await LOGGER.logger(f"please use these keys: {parameter_list[1]}")
        await run_exit(LOGGER)
    return [True for item in range(3)]


async def check_root_keys(env_object):
    list_root_keys = ROOT_KEYS
    response = await verification([list(env_object.keys()), list_root_keys])
    if all(response):
        return (env_object.get(AZURE), env_object.get(COSMO))
    await run_exit(LOGGER)


async def check_azure_keys(azure):
    list_azure_keys = AZURE_KEYS

    if not azure:
        await LOGGER.logger(f'please add keys in azure section: {list_azure_keys}')
        await run_exit(LOGGER)

    response = await verification([azure, list_azure_keys])
    if all(response):
        return azure
    await run_exit(LOGGER)

async def check_cosmo_keys(cosmo):
    list_cosmo_keys = COSMO_KEYS

    if not cosmo:
        await LOGGER.logger(f'please add keys in cosmo section: {list_cosmo_keys}')
        await run_exit(LOGGER)

    response = await verification([cosmo, list_cosmo_keys])
    if all(response):
        if not cosmo.get(SCENARIOS):
            await LOGGER.logger("no scenarios in config file")
            await run_exit(LOGGER)
        return cosmo
    await run_exit(LOGGER)

async def check_cosmo_scenarios_keys(item):
    list_keys = SCENARIOS_KEYS

    if not item:
        await LOGGER.logger(f'please add a list of scenario in scenarios section: {list_keys}')
        await run_exit(LOGGER)

    response = await verification([item, list_keys])
    if all(response):
        return item
    await run_exit(LOGGER)

async def check_dataset_keys(dataset):
    list_keys = DATASET_KEYS

    if not dataset:
        await LOGGER.logger(f'please add keys in datasets section: {list_keys}')
        await run_exit(LOGGER)

    for d in dataset:
        response = await verification([d, list_keys])
        if all(response):
            return dataset
    await run_exit(LOGGER)

async def check_scenario_structure():
    cosmo = SERVICES.cosmo.get(SCENARIOS)
    for k,item in enumerate(cosmo):
        check_type = cosmo[k]
        if isinstance(check_type, str):
            await run_exit(LOGGER)

        # check scenario keys
        await check_cosmo_scenarios_keys(cosmo[k])

async def check_cosmo_connector_keys(type):
    if not type:
        await LOGGER.logger(f"please add connector")
        await run_exit(LOGGER)
    return type

async def check_cosmo_organization_keys(organization):
    if not organization:
        await LOGGER.logger(f"please add an id in organization section")
        await run_exit(LOGGER)
    return organization

async def check_cosmo_workspace_keys(workspace):
    if not workspace:
        await LOGGER.logger(f'please add an id in workspace section')
        await run_exit(LOGGER)
    return workspace

import sys
async def check_all_keys_in_config_file(env_object):
    azure, cosmo = await check_root_keys(env_object)
    azure = await check_azure_keys(azure)
    cosmo = await check_cosmo_keys(cosmo)
    SERVICES.set_azure(azure)
    SERVICES.set_cosmo(cosmo)

    organization_id = await check_cosmo_organization_keys(cosmo.get(ORGANIZATION_ID))
    organization = await check_organization_by_id(organization_id)
    SERVICES.set_organization(organization)
    
    workspace_id = await check_cosmo_workspace_keys(cosmo.get(WORKSPACE_ID))
    workspace = await check_workspace_by_id(workspace_id)
    SERVICES.set_workspace(workspace)
    SERVICES.set_runtemplate(workspace.run_template_filter)

    solution = await check_solution_by_id(workspace.solution.solution_id)
    SERVICES.set_solution(solution)
    
    connector_type = await check_cosmo_connector_keys(cosmo.get(CONNECTOR))
    connector = await get_connectors(connector_type)
    SERVICES.set_connector(connector)

    datasets = await check_dataset_keys(cosmo.get(DATASET))
    SERVICES.set_datasets(datasets)
