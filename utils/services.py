from utils.constants import NAME
from utils.singleton import SingletonType

class Services(object, metaclass=SingletonType):
    azure = {}
    cosmo = {}
    organization = {}
    workspace = {}
    solution = {}
    connector = {}
    datasets = []
    run_template = []

    # data for run logs
    scenarios = []
    scenarios_created = []
    datasets_id = []
    run_scenarios = []

    # run supply or asset ?
    run_supply: bool = True
    run_asset: bool = False

    def set_run_supply(self, value):
        self.run_supply = value

    def set_run_asset(self, value):
        self.run_asset = value
    
    def set_azure(self,azure):
        self.azure = azure

    def set_cosmo(self,cosmo):
        self.cosmo = cosmo

    def set_organization(self,organization):
        self.organization = organization

    def set_workspace(self,workspace):
        self.workspace = workspace

    def set_solution(self,solution):
        self.solution = solution

    def set_datasets(self,datasets):
        self.datasets = datasets

    def set_connector(self,connector):
        self.connector = connector

    def set_runtemplate(self,template):
        self.run_template = template

    # data for logs
    def set_scenarios(self,scenarios):
        self.scenarios.append(scenarios)

    def set_scenario_created(self, scenario_created):
        self.scenarios_created.append(scenario_created)

    def set_datasets_id(self, datasets_id):
        self.datasets_id.append(datasets_id)

    def set_run_scenarios(self, run_scenarios):
        self.run_scenarios = run_scenarios
    # data for logs

    async def __get_dataset_by_name__(self, name):
        dataset = list(filter(lambda d: d.get(NAME).lower() == name.lower(), self.datasets))
        if len(dataset) >= 1:
            return dataset[0]