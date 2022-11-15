""".env"""
import sys
import zipfile
from decouple import config
from azure.storage.blob import BlobServiceClient

CONTAINER_NAME_DATASETS = "performance-datasets"

def download_files(name_file_storage: str):
    """Download files from storaget performance container datasets"""
    connection_string = config('CONNECTION_STRING')
    # blob connection client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_id_lower = str(CONTAINER_NAME_DATASETS).lower()
    container_client = blob_service_client.get_container_client(container_id_lower)
    blob = blob_service_client.get_blob_client(container_id_lower, name_file_storage)
    if not blob.exists():
        print(f"blob {name_file_storage} not exist")
        sys.exit(1)

    blob_name = name_file_storage
    with open(file=f"./data/{blob_name}", mode="wb") as download_file:
        download_file.write(container_client.download_blob(blob_name).readall())

    with zipfile.ZipFile(f"./data/{blob_name}") as zip_file:
        zip_file.extractall("./data")
    return True