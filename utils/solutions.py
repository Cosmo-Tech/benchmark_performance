"""Solution cosmotech api"""
import sys
from cosmotech_api import ApiException
from cosmotech_api.api import solution_api

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.services import Services
SERVICES = Services.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()

async def check_solution_by_id():
    api_client = await COSMO_API.__get_api__()
    api_instance = solution_api.SolutionApi(api_client)
    try:
        api_response = api_instance.find_solution_by_id(SERVICES.organization.get('id'), SERVICES.solution.get('id'))
        return bool(api_response)
    except ApiException as _exception:
        await LOGGER.logger(f"The solution with: '{SERVICES.solution.get('id')}' does not exist")
        return False
