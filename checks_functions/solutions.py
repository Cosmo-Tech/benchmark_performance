""".env"""
import sys
from cosmotech_api import ApiException
from cosmotech_api.api import solution_api
sys.dont_write_bytecode=True

def check_solution_by_id(api_client: object, organization_id: str, solution_id: str) -> bool:
    """.env"""
    api_instance = solution_api.SolutionApi(api_client)
    try:
        api_response = api_instance.find_solution_by_id(organization_id, solution_id)
        return bool(api_response)
    except ApiException as _exception:
        print(f"The solution with: '{solution_id}' does not exist")
        return False
