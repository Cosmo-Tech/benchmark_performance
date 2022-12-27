""".env"""
from cosmotech_api import ApiException
from cosmotech_api.api import scenario_api
from utils.run_exit import run_exit

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.validation_config_file import Services
SERVICES = Services.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()

async def delete_scenario(scenario_id):

    api_client = await COSMO_API.__get_api__()
    scenario_api_instance = scenario_api.ScenarioApi(api_client)
    try:
        scenario_api_instance.delete_scenario(
            SERVICES.organization.get('id'),
            SERVICES.workspace.get('id'),
            scenario_id
        )
        await LOGGER.logger(f"scenario with id {scenario_id} deleted")
    except ApiException as exception:
        await LOGGER.logger(f"Exception when calling ScenarioApi->delete_scenario: {exception}")
        await run_exit(LOGGER)