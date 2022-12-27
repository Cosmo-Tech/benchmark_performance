"""Connector cosmotech api"""
import sys
from cosmotech_api import ApiException
from cosmotech_api.api import connector_api
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
        await logger.logger(api_response.key)
        return api_response.key
    except ApiException as _exception:
        await logger.logger(f"The connector with: {connector_id} not exist")
        await run_exit(logger)
