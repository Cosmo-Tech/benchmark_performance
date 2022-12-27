""".env"""
import sys
import zipfile
from decouple import config
from azure.storage.blob import BlobServiceClient

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.services import Services
SERVICES = Services.__call__()

from utils.path import Path
PATH = Path.__call__()

CONTAINER_NAME_DATASETS = "performance-datasets"

async def download_files():
    """Download files from storaget performance container datasets"""
    connection_string = config('CONNECTION_STRING')
    # blob connection client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_id_lower = str(CONTAINER_NAME_DATASETS).lower()
    container_client = blob_service_client.get_container_client(container_id_lower)
    blob = blob_service_client.get_blob_client(container_id_lower, SERVICES.cosmo.get('name_file_storage'))
    if not blob.exists():
        await LOGGER.logger(f"blob {SERVICES.cosmo.get('name_file_storage')} not exist")
        sys.exit(1)

    blob_name = SERVICES.cosmo.get('name_file_storage')
    with open(file=f"{PATH.DATA}/{blob_name}", mode="wb") as download_file:
        download_file.write(container_client.download_blob(blob_name).readall())

    with zipfile.ZipFile(f"{PATH.DATA}/{blob_name}") as zip_file:
        zip_file.extractall(PATH.DATA)
    return True
