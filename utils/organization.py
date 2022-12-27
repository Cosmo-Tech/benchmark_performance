"""Organization cosmotech api"""
import sys
import pandas as pd
from cosmotech_api import ApiException
from cosmotech_api.api import organization_api

from utils.logger import Logger
logger = Logger.__call__()

from utils.services import Services
SERVICES = Services.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()

async def check_organization_by_id():
    api_client = await COSMO_API.__get_api__()
    api_instance = organization_api.OrganizationApi(api_client)    
    try:
        api_response = api_instance.find_all_organizations()
        data = [item.to_dict() for item in api_response]
        df_organization = pd.DataFrame(data)
    except ApiException as exception:
        await logger.logger(f"Exception when calling Api: {exception}")
        return False
    result = df_organization.loc[df_organization['id']==SERVICES.organization.get('id')]
    if result.empty:
        await logger.logger(f"There is no organization with id : {SERVICES.organization.get('id')}")
        return False
    return not(result.empty)
