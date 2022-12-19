""".env"""
import os
import sys
from decouple import config
from cosmotech_api import ApiException
from cosmotech_api.api import dataset_api
from azure.storage.blob import BlobServiceClient
from utils.logger import Logger

logger = Logger.__call__()

async def delete_dataset_workspace(services: object, dataset_input: str, dataset_id: str):
    """delete datatset on workspace storage blob"""
    path_data = services.paths.data
    connection_string = config('CONNECTION_STRING')
    # blob connection client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    organization_id_lower = str(services.organization.id).lower()
    workspace_id_lower = str(services.workspace.id).lower()

    container_client = blob_service_client.get_container_client(organization_id_lower)

    directory_name_in_storage = f"{workspace_id_lower}/datasets/{dataset_id}"

    local_dir_dataset = f"{path_data}/{dataset_input}/dataset"
    for csv_file in os.listdir(local_dir_dataset):
        filename = os.path.join(directory_name_in_storage, csv_file)
        container_client.delete_blob(filename)

    await delete_scenario_http_request(services, dataset_id)
    await logger.logger(f"clean up dataset with id: {dataset_id}")


async def delete_scenario_http_request(services: object, dataset_id: str):
    """Delete scenario from database"""
    dataset_api_instance = dataset_api.DatasetApi(services.api_client)
    try:
        dataset_api_instance.delete_dataset(services.organization.id, dataset_id)
    except ApiException as exception:
        await logger.logger(f"Exception when calling DatasetApi->delete_scenario: {exception}")
        sys.exit(1)
