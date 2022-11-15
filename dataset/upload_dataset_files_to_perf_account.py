""".env"""
import os
from decouple import config
from azure.storage.blob import BlobServiceClient
from storage.create_container import create_container_upsert

def upload_files(services:object, dataset_id: str, scenario_directory: str):
    """upload files to storage container"""

    connection_string = config('CONNECTION_STRING')

    # Create a blob service client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # path blob name
    organizarion_id_lower = str(services.organization_id).lower()
    workspace_id_lower = str(services.workspace_id).lower()
    dataset_id_id_lower = str(dataset_id).lower()

    # create is not exists
    create_container_upsert(organizarion_id_lower)

    for dataset_csv_file in os.listdir(f"./data/{scenario_directory}/dataset"):
        # for each file in dataset
        blob_client = blob_service_client.get_blob_client(
            container=f"{organizarion_id_lower}",
            blob=f"{workspace_id_lower}/datasets/{dataset_id_id_lower}/{dataset_csv_file}"
        )
        with open(f"./data/{scenario_directory}/dataset/{dataset_csv_file}", "rb") as data:
            blob_client.upload_blob(data)
