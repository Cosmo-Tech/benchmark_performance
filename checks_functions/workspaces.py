"""Workspace cosmotech api"""
import sys
from cosmotech_api import ApiException
from cosmotech_api.api import workspace_api
sys.dont_write_bytecode=True

def check_workspace_by_id(api_client, organization_id, workspace_id: str) -> bool:
    """check if workspace id exist in cosmotech"""
    api_instance = workspace_api.WorkspaceApi(api_client)
    try:
        api_response = api_instance.find_workspace_by_id(organization_id, workspace_id)
        return bool(api_response)
    except ApiException as _exception:
        print(f"The workspace with: '{workspace_id}' does not exist")
        return False
