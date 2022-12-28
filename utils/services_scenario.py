import concurrent.futures
from time import perf_counter
from scenario_run.run_scenario_flow import run_scenario_flow
from utils.constants import CLIENT_ID, CLIENT_SECRET, COSMO_API_HOST, COSMO_API_SCOPE, TENANT_ID
from utils.singleton import SingletonType

from utils.services import Services
SERVICES = Services.__call__()

class ServicesScenarios(object, metaclass=SingletonType):
    scenarios = []
    async def set_scenarios(self, scenario):
        self.scenarios.append(scenario)

    async def run_scenario_async(self):

        tenant_id = SERVICES.azure.get(TENANT_ID)
        client_id = SERVICES.azure.get(CLIENT_ID)
        client_secret = SERVICES.azure.get(CLIENT_SECRET)
        cosmo_api_host = SERVICES.azure.get(COSMO_API_HOST)
        cosmo_api_scope = SERVICES.azure.get(COSMO_API_SCOPE)

        organization_id = SERVICES.organization.get('id')
        workspace_id = SERVICES.workspace.get('id')

        run_ids = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = { executor.submit(run_scenario_flow,
                organization_id,
                workspace_id,
                scenario_id,
                tenant_id, 
                client_id, 
                client_secret, 
                cosmo_api_host, 
                cosmo_api_scope) for scenario_id in self.scenarios }

            for f in concurrent.futures.as_completed(results):
                try:
                    run_ids.append(f.result())                
                except Exception as exc:
                    print("Exception", exc)

        return run_ids