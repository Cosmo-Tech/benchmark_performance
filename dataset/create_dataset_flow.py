""".env"""
from decouple import config
from cosmotech_api.api import dataset_api
from cosmotech_api import ApiException
from cosmotech_api.model.dataset import Dataset
from cosmotech_api.model.dataset_connector import DatasetConnector
from dataset.upload_dataset_files_to_perf_account import upload_files
from utils.logger import Logger

logger = Logger.__call__()

async def create_dataset_http_request(dataset_api_instance, organization_id, dataset_object):
    """create dataset request to cosmotech api"""
    try:
        dataset_created = dataset_api_instance.create_dataset(organization_id, dataset_object)
        await logger.logger(f"dataset with id  {dataset_created.id} created")
        return dataset_created
    except ApiException as exception:
        await logger.logger(f"Exception when calling DatasetApi->create_dataset: {exception}")
        return None

def build_dataset_object(scenario: object, services):
    """Build dataset object: dataset name of config file yml"""
    return Dataset(
        name=scenario.dataset.name,
        description="description_example_perf",
        tags=[
            "Performance Test CosmoTest",
        ],
        connector=DatasetConnector(
            id=services.connector.id,
        ),
    )

def upload_local_files_to_azure_storage_container(
        services: object,
        scenario: object,
        dataset_id: str
    ):
    """upload file to azure storage container"""
    upload_files(services, dataset_id, f"{scenario.dataset.path_input}")

def build_dataset_with_connector(connector, dataset_created):
    """build dataset with connector"""
    connector_url = connector.url
    if connector.type == "ADT Connector":
        dataset_created.connector = DatasetConnector(
                id=connector.id,
                parameters_values= {
                    "AZURE_DIGITAL_TWINS_URL": connector_url
                }
            )
    else:
        blob_name = f"%WORKSPACE_FILE%/datasets/{dataset_created.id}"
        dataset_created.connector = DatasetConnector(
                id=connector.id,
                parameters_values= {
                    "AZURE_STORAGE_CONNECTION_STRING": f"{config('CONNECTION_STRING')}",
                    "AZURE_STORAGE_CONTAINER_BLOB_PREFIX": blob_name
                }
            )
    return dataset_created

async def update_dataset_files_in_azure_storage_container(
        dataset_api_instance,
        organization_id,
        dataset_created_with_connector
    ):
    """update dataset files in azure storage container"""
    try:
        dataset_updated = dataset_api_instance.update_dataset(
            organization_id,
            dataset_created_with_connector.id,
            dataset_created_with_connector)
        await logger.logger(f"dataset with id {dataset_updated.id} updated")
    except ApiException as exception:
        await logger.logger(f"Exception when calling DatasetApi->update_dataset: {exception}")
        return None


async def create_dataset_flow(services: object, scenario: object):
    """create dataset flow: buidl object, creation request, update with connector and upload to storage"""
    dataset_api_instance = dataset_api.DatasetApi(services.api_client)

    dataset_object = build_dataset_object(scenario, services)
    dataset_created = await create_dataset_http_request(
        dataset_api_instance,
        services.organization.id,
        dataset_object
    )
    dataset_created_with_connector = build_dataset_with_connector(
        services.connector,
        dataset_created
    )
    if services.connector.type != "ADT Connector":
        upload_local_files_to_azure_storage_container(
            services,
            scenario,
            dataset_created_with_connector.id
        )

    await update_dataset_files_in_azure_storage_container(
        dataset_api_instance,
        services.organization.id,
        dataset_created_with_connector
    )

    return dataset_created_with_connector.id
