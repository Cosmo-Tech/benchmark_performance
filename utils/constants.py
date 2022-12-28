# keys configuration file
AZURE = "azure"
COSMO = "cosmo"
ROOT_KEYS = [ AZURE, COSMO]

TENANT_ID = "tenant_id"
CLIENT_ID = "client_id"
CLIENT_SECRET = "client_secret"
COSMO_API_SCOPE = "cosmo_api_scope"
COSMO_API_HOST = "cosmo_api_host"

AZURE_KEYS = [
    TENANT_ID,
    CLIENT_ID,
    CLIENT_SECRET,
    COSMO_API_SCOPE,
    COSMO_API_HOST
]

ORGANIZATION_ID = "organization_id"
WORKSPACE_ID = "workspace_id"
CONNECTOR = "connector"
DATASET = "dataset"
SCENARIOS = "scenarios"

COSMO_KEYS = [
    ORGANIZATION_ID,
    WORKSPACE_ID,
    CONNECTOR,
    DATASET,
    SCENARIOS
]

NAME = "name"
PATH_INPUT = "path_input"
DATASET_KEYS = [
    NAME,
    PATH_INPUT
]

SIZE = "size"
COMPUTE_SIZE = "compute_size"

SCENARIOS_KEYS = [
    NAME,
    SIZE,
    COMPUTE_SIZE,
    DATASET,
]

CONFIGURATION_FILENAME = "cosmotest.config.yml"
CONTAINER_DATASET = "performance-datasets"
CONTAINER_RESULT = "performance-results"
ACCOUNT_NAME = "ACCOUNT_NAME"
ACCOUNT_KEY = "ACCOUNT_KEY"
CONNECTION_STRING = "CONNECTION_STRING"

CONNECTOR_AZURE_KEY = "AzureStorageConnector"
CONNECTOR_ADT_KEY = "ADT Connector"

DATA_FOLDER = "data"
LOGS_FOLDER= "logs"
SUMMARY_FOLDER = "summary"
INPUT_FOLDER = "input"

DATASET_FOLDER = 'dataset'
SCENARIO_FOLDER= "scenario"
MASS_LEVER_EXCEL_FILE = "mass_lever_excel_file"
DEMAND_PLAN = "demand_plan"
PRODUCTION_RESOURCE_OPENING_TIME = "production_resource_opening_time"
TRANSPORT_DURATION = "transport_duration"

PERFORMANCE_TEST_CSV = "performance-test.csv"
PERFORMANCE_STEPS_CSV = "performance-steps.csv"
PERFORMANCE_CAPACITY_CSV = "performance-capacity.csv"
CONTAINER_NAME_RESULTS = "performance-results"
SUMMARY_ZIP_NAME = "results-summary.zip"

TAGS_DATASET = ["ADT", "dataset"]
TAGS_DATASET_PERFORMANCE_TEST = ['Performance Test CosmoTest']

ITEMS_COMPUTE_SIZE = ["highcpu", "basic", "memory"]