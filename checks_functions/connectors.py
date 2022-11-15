"""Connector cosmotech api"""
import sys
from cosmotech_api import ApiException
from cosmotech_api.api import connector_api
sys.dont_write_bytecode=True

def check_connector_by_id(api_client, connector_id: str) -> bool:
    """check if connector id exist"""
    api_instance = connector_api.ConnectorApi(api_client)
    try:
        api_response = api_instance.find_connector_by_id(connector_id)
        return bool(api_response)
    except ApiException as _exception:
        print(f"The connector with: {connector_id} not exist")
        return False
