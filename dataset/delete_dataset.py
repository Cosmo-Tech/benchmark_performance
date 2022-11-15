""".env"""
import os
import sys
from decouple import config
from cosmotech_api import ApiException
from cosmotech_api.api import dataset_api
from azure.storage.blob import BlobServiceClient

def delete_dataset_workspace(services: object, dataset_input: str, dataset_id: str):
    """.env"""
    connection_string = config('CONNECTION_STRING')
    # blob connection client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    organization_id_lower = str(services.organization_id).lower()
    workspace_id_lower = str(services.workspace_id).lower()

    container_client = blob_service_client.get_container_client(organization_id_lower)

    directory_name_in_storage = f"{workspace_id_lower}/datasets/{dataset_id}"

    local_dir_dataset = f"./data/{dataset_input}/dataset"
    for csv_file in os.listdir(local_dir_dataset):
        filename = os.path.join(directory_name_in_storage, csv_file)
        container_client.delete_blob(filename)

    delete_scenario_http_request(services, dataset_id)
    print("clean up dataset with id:", dataset_id)


def delete_scenario_http_request(services: object, dataset_id: str):
    """Delete scenario from database"""
    dataset_api_instance = dataset_api.DatasetApi(services.api_client)
    try:
        dataset_api_instance.delete_dataset(services.organization_id, dataset_id)
    except ApiException as exception:
        print(f"Exception when calling DatasetApi->delete_scenario: {exception}")
        sys.exit(1)
