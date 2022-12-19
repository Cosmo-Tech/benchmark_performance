"""Solution cosmotech api"""
import sys
from cosmotech_api import ApiException
from cosmotech_api.api import solution_api
from utils.logger import Logger
sys.dont_write_bytecode=True

logger = Logger.__call__()

async def check_solution_by_id(api_client: object, organization_id: str, solution_id: str) -> bool:
    """check if solution exist"""
    api_instance = solution_api.SolutionApi(api_client)
    try:
        api_response = api_instance.find_solution_by_id(organization_id, solution_id)
        return bool(api_response)
    except ApiException as _exception:
        await logger.logger(f"The solution with: '{solution_id}' does not exist")
        return False
