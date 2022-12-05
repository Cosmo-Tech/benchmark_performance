""".env"""
from cosmotech_api import ApiException
from cosmotech_api.api import scenario_api

def delete_scenario(services, scenario_id):
    """delete scenario by id"""
    scenario_api_instance = scenario_api.ScenarioApi(services.api_client)
    try:
        scenario_api_instance.delete_scenario(
            services.organization.id,
            services.workspace.id,
            scenario_id
        )
        print("scenario with id "+ scenario_id + " deleted")
    except ApiException as exception:
        print(f"Exception when calling ScenarioApi->delete_scenario: {exception}")
        