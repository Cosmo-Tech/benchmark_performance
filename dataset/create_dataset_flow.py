from decouple import config
from cosmotech_api.api import dataset_api
from cosmotech_api import ApiException
from cosmotech_api.model.dataset import Dataset
from cosmotech_api.model.dataset_connector import DatasetConnector
from dataset.upload_dataset_files_to_perf_account import upload_files
from dataset.create_request import create_dataset_http_request
from utils.constants import CONNECTION_STRING, CONNECTOR_ADT_KEY, NAME, PATH_INPUT

from utils.path import Path
PATH = Path.__call__()

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.validation_config_file import Services
SERVICES = Services.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()

def build_dataset_object(dataset):
    return Dataset(
        name=dataset.get(NAME),
        description="description_example_perf",
        tags=[ "Performance Test CosmoTest" ],
        connector=DatasetConnector(
            id=SERVICES.connector.get('id'),
        ),
    )

def upload_local_files_to_azure_storage_container(dataset, dataset_id):
    upload_files(dataset_id, f"{dataset.get(PATH_INPUT)}")

def build_dataset_with_connector(dataset_created):
    connector_url = SERVICES.connector.get('url')
    if SERVICES.connector.get('type') == CONNECTOR_ADT_KEY:
        dataset_created.connector = DatasetConnector(
                id=SERVICES.connector.get('id'),
                parameters_values= {
                    "AZURE_DIGITAL_TWINS_URL": connector_url
                }
            )
    else:
        blob_name = f"%WORKSPACE_FILE%/datasets/{dataset_created.id}"
        dataset_created.connector = DatasetConnector(
                id=SERVICES.connector.get('id'),
                parameters_values= {
                    "AZURE_STORAGE_CONNECTION_STRING": f"{config(CONNECTION_STRING)}",
                    "AZURE_STORAGE_CONTAINER_BLOB_PREFIX": blob_name
                }
            )
    return dataset_created

async def update_dataset_files_in_azure_storage_container(
        dataset_api_instance,
        dataset_created_with_connector
    ):
    try:
        dataset_updated = dataset_api_instance.update_dataset(
            SERVICES.organization.get('id'),
            dataset_created_with_connector.id,
            dataset_created_with_connector)
        await LOGGER.logger(f"dataset with id {dataset_updated.id} updated")
    except ApiException as exception:
        await LOGGER.logger(f"Exception when calling DatasetApi->update_dataset: {exception}")
        return None


async def create_dataset_flow(dataset):

    api_client = await COSMO_API.__get_api__()
    dataset_api_instance = dataset_api.DatasetApi(api_client)

    dataset_object = build_dataset_object(dataset)

    dataset_created = await create_dataset_http_request(
        dataset_api_instance,
        dataset_object
    )

    dataset_created_with_connector = build_dataset_with_connector(
        dataset_created
    )
    
    if SERVICES.connector.get('type') != CONNECTOR_ADT_KEY:
        upload_local_files_to_azure_storage_container(
            dataset,
            dataset_created_with_connector.id
        )

    await update_dataset_files_in_azure_storage_container(
        dataset_api_instance,
        dataset_created_with_connector
    )

    return dataset_created_with_connector.id
