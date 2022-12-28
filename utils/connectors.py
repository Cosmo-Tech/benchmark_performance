from cosmotech_api import ApiException
from cosmotech_api.api import connector_api
from utils.constants import *
from utils.run_exit import run_exit

from utils.logger import Logger
logger = Logger.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()

async def check_connector_by_id(connector_id):

    api_client = await COSMO_API.__get_api__()
    api_instance = connector_api.ConnectorApi(api_client)
    
    try:
        api_response = api_instance.find_connector_by_id(connector_id)
        return api_response.key
    except ApiException as _exception:
        await logger.logger(f"the connector with: {connector_id} not exist")
        await run_exit(logger)

async def get_connectors(type):
    api_client = await COSMO_API.__get_api__()
    api_instance = connector_api.ConnectorApi(api_client)
    key = CONNECTOR_AZURE_KEY if type.lower() == 'AKS'.lower() else CONNECTOR_ADT_KEY
    try:
        api_response = api_instance.find_all_connectors()
        aks_connectors = list(filter(lambda c: key in c.key, api_response))
        last = max(aks_connectors, key= lambda k : k.version)
        return last
    except ApiException as _exception:
        await run_exit(logger)