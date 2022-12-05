""".env"""
from cosmotech_api.api import scenariorun_api

def run_scenario_flow(services, scenario_id):
    """Run scenario flow: run request cosmotech api"""
    scenario_run_api_instance = scenariorun_api.ScenariorunApi(services.api_client)

    scenario_run_object = scenario_run_api_instance.run_scenario(
        organization_id=services.organization.id,
        workspace_id=services.workspace.id,
        scenario_id=scenario_id
    )
    return scenario_run_object
