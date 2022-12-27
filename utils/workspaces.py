"""Workspace cosmotech api"""
import sys
from cosmotech_api import ApiException
from cosmotech_api.api import workspace_api
from utils.run_exit import run_exit

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.services import Services
SERVICES = Services.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()

async def check_workspace_by_id():
    api_client = await COSMO_API.__get_api__()
    api_instance = workspace_api.WorkspaceApi(api_client)
    try:
        api_response = api_instance.find_workspace_by_id(SERVICES.organization.get('id'), SERVICES.workspace.get('id'))
        return bool(api_response)
    except ApiException as _exception:
        await LOGGER.logger(f"The workspace with: '{SERVICES.workspace.get('id')}' does not exist")
        await run_exit(LOGGER)
