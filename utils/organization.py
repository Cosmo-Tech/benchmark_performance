"""Organization cosmotech api"""
import sys
import pandas as pd
from cosmotech_api import ApiException
from cosmotech_api.api import organization_api
from utils.logger import Logger
sys.dont_write_bytecode=True

logger = Logger.__call__()

async def check_organization_by_id(api_client, organization_id: str) -> bool:
    """check if organization exist"""
    api_instance = organization_api.OrganizationApi(api_client)    
    try:
        api_response = api_instance.find_all_organizations()
        data = [item.to_dict() for item in api_response]
        df_organization = pd.DataFrame(data)
    except ApiException as exception:
        await logger.logger(f"Exception when calling Api: {exception}")
        return False
    result = df_organization.loc[df_organization['id']==organization_id]
    if result.empty:
        await logger.logger(f"There is no organization with id : {organization_id}")
        return False
    return not(result.empty)
