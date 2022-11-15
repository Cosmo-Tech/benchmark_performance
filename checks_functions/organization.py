""".env"""
import sys
import pandas as pd
from cosmotech_api import ApiException
from cosmotech_api.api import organization_api 
sys.dont_write_bytecode=True

def check_organization_by_id(api_client, organization_id: str) -> bool:
    """.env"""
    api_instance = organization_api.OrganizationApi(api_client)    
    try:
        api_response = api_instance.find_all_organizations()
        data = [item.to_dict() for item in api_response]
        df_organization = pd.DataFrame(data)
    except ApiException as exception:
        print(f"Exception when calling Api: {exception}")
        return False
    result = df_organization.loc[df_organization['id']==organization_id]
    if result.empty:
        print(f"There is no organization with id : {organization_id}")
        return False
    return not(result.empty)
