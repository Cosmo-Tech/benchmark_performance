from cosmotech_api import ApiException
from cosmotech_api.api import organization_api
from utils.run_exit import run_exit

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.services import Services
SERVICES = Services.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()

async def check_organization_by_id(id):
    api_client = await COSMO_API.__get_api__()
    api_instance = organization_api.OrganizationApi(api_client)    
    try:
        api_response = api_instance.find_organization_by_id(id)
        return api_response
    except ApiException as exception:
        await LOGGER.logger(f"the organization with: '{id}' not exist")
        await run_exit(LOGGER)
