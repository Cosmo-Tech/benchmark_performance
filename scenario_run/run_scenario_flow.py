from cosmotech_api import ApiClient
from azure.identity import ClientSecretCredential
from utils.configuration import get_configuration
from cosmotech_api.api import scenariorun_api

def run_scenario_flow(
        organization_id,
        workspace_id,
        scenario_id,
        tenant_id,
        client_id, 
        client_secret,
        cosmo_api_host,
        cosmo_api_scope
    ):

    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    token = credential.get_token(cosmo_api_scope).token
    configuration = get_configuration(cosmo_api_host, token)
    api_client = ApiClient(configuration)

    scenario_run_api_instance = scenariorun_api.ScenariorunApi(api_client)

    scenario_run_object = scenario_run_api_instance.run_scenario(
        organization_id=organization_id,
        workspace_id=workspace_id,
        scenario_id=scenario_id
    )
    return scenario_run_object.id
