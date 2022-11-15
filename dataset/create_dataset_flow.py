""".env"""
from decouple import config
from cosmotech_api.api import dataset_api
from cosmotech_api import ApiException
from cosmotech_api.model.dataset import Dataset
from cosmotech_api.model.dataset_connector import DatasetConnector
from dataset.upload_dataset_files_to_perf_account import upload_files

def create_dataset_http_request(dataset_api_instance, organization_id, dataset_object):
    """.env"""
    try:
        dataset_created = dataset_api_instance.create_dataset(organization_id, dataset_object)
        print(f"dataset with id  {dataset_created.id} created")
        return dataset_created
    except ApiException as exception:
        print(f"Exception when calling DatasetApi->create_dataset: {exception}")
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
            id=services.connector_id,
        ),
    )

def upload_local_files_to_azure_storage_container(
        services: object,
        scenario: object,
        dataset_id: str
    ):
    """.env"""
    upload_files(services, dataset_id, f"{scenario.dataset.path_input}")


def build_dataset_with_connector(connector_id, dataset_created):
    """.env"""

    blob_name = f"%WORKSPACE_FILE%/datasets/{dataset_created.id}"
    dataset_created.connector = DatasetConnector(
            id=connector_id,
            parameters_values= {
                "AZURE_STORAGE_CONNECTION_STRING": f"{config('CONNECTION_STRING')}",
                "AZURE_STORAGE_CONTAINER_BLOB_PREFIX": blob_name
            }
        )
    return dataset_created

def update_dataset_files_in_azure_storage_container(
        dataset_api_instance,
        organization_id,
        dataset_created_with_connector
    ):
    """.env"""
    try:
        dataset_updated = dataset_api_instance.update_dataset(
            organization_id,
            dataset_created_with_connector.id,
            dataset_created_with_connector)
        print(f"dataset with id {dataset_updated.id} updated")
    except ApiException as exception:
        print(f"Exception when calling DatasetApi->update_dataset: {exception}")
        return None


def create_dataset_flow(services: object, scenario: object):
    """.env"""
    dataset_api_instance = dataset_api.DatasetApi(services.api_client)

    dataset_object = build_dataset_object(scenario, services)
    dataset_created = create_dataset_http_request(
        dataset_api_instance,
        services.organization_id,
        dataset_object
    )
    dataset_created_with_connector = build_dataset_with_connector(
        services.connector_id,
        dataset_created
    )
    upload_local_files_to_azure_storage_container(
        services,
        scenario,
        dataset_created_with_connector.id
    )
    update_dataset_files_in_azure_storage_container(
        dataset_api_instance,
        services.organization_id,
        dataset_created_with_connector
    )

    return dataset_created_with_connector.id
