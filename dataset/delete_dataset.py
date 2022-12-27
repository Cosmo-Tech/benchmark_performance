""".env"""
import os
import sys
from decouple import config
from cosmotech_api import ApiException
from cosmotech_api.api import dataset_api
from azure.storage.blob import BlobServiceClient
from utils.run_exit import run_exit

from utils.path import Path
PATH = Path.__call__()

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.validation_config_file import Services
SERVICES = Services.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()

async def delete_dataset_workspace(dataset_input: str, dataset_id: str):
    """delete datatset on workspace storage blob"""
    path_data = PATH.DATA
    connection_string = config('CONNECTION_STRING')
    # blob connection client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    organization_id_lower = str(SERVICES.organization.get('id')).lower()
    workspace_id_lower = str(SERVICES.workspace.get('id')).lower()

    container_client = blob_service_client.get_container_client(organization_id_lower)

    directory_name_in_storage = f"{workspace_id_lower}/datasets/{dataset_id}"

    local_dir_dataset = f"{path_data}/{dataset_input}/dataset"
    for csv_file in os.listdir(local_dir_dataset):
        filename = os.path.join(directory_name_in_storage, csv_file)
        container_client.delete_blob(filename)

    await delete_scenario_http_request(dataset_id)
    await LOGGER.logger(f"clean up dataset with id: {dataset_id}")


async def delete_scenario_http_request(dataset_id):
    api_client = await COSMO_API.__get_api__()
    dataset_api_instance = dataset_api.DatasetApi(api_client)
    try:
        dataset_api_instance.delete_dataset(SERVICES.organization.get('id'), dataset_id)
    except ApiException as exception:
        await LOGGER.logger(f"Exception when calling DatasetApi->delete_scenario: {exception}")
        await run_exit(LOGGER)