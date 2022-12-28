import os
import glob
import zipfile
from decouple import config
from utils.run_exit import run_exit

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.services import Services
SERVICES = Services.__call__()

from utils.path import Path
PATH = Path.__call__()

from utils.services_storage import ServiceStorage
SERVICE_STORAGE = ServiceStorage.__call__()

async def download_files():

    container_id_lower = str(SERVICE_STORAGE.container_dataset).lower()
    container_client = SERVICE_STORAGE.blob_service_client.get_container_client(container_id_lower)
    
    blob = SERVICE_STORAGE.blob_service_client.get_blob_client(container_id_lower, PATH.zip_file)
    if not blob.exists():
        await LOGGER.logger(f"blob {PATH.zip_file} not exist")
        await run_exit(LOGGER)

    with open(file=f"{PATH.DATA}/{PATH.zip_file}", mode="wb") as download_file:
        download_file.write(container_client.download_blob(PATH.zip_file).readall())

    with zipfile.ZipFile(f"{PATH.DATA}/{PATH.zip_file}") as zip_file:
        zip_file.extractall(PATH.DATA)
    
    os.remove(f"{PATH.DATA}/{PATH.zip_file}")

