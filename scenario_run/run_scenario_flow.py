from cosmotech_api.api import scenariorun_api

from utils.validation_config_file import Services
SERVICES = Services.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()

async def run_scenario_flow(scenario_id):

    api_client = await COSMO_API.__get_api__()
    scenario_run_api_instance = scenariorun_api.ScenariorunApi(api_client)

    scenario_run_object = scenario_run_api_instance.run_scenario(
        organization_id=SERVICES.organization.get('id'),
        workspace_id=SERVICES.workspace.get('id'),
        scenario_id=scenario_id
    )
    return scenario_run_object
