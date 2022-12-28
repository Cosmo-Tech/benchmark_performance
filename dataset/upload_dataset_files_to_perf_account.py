import os
from decouple import config
from storage.create_container import create_container_upsert
from utils.run_exit import run_exit
from utils.constants import DATASET_FOLDER, MASS_LEVER_EXCEL_FILE, NAME, SCENARIO_FOLDER

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.path import Path
PATH = Path.__call__()

from utils.validation_config_file import Services
SERVICES = Services.__call__()

from utils.services_storage import ServiceStorage
SERVICE_STORAGE = ServiceStorage.__call__()

def upload_files(dataset_id: str, dataset_directory: str):
    
    # path blob name
    organizarion_id_lower = str(SERVICES.organization.get('id')).lower()
    workspace_id_lower = str(SERVICES.workspace.get('id')).lower()
    dataset_id_id_lower = str(dataset_id).lower()

    # create is not exists
    create_container_upsert(organizarion_id_lower)

    for dataset_file in os.listdir(f"{PATH.DATA}/{DATASET_FOLDER}/{dataset_directory}"):
        if os.path.isdir(f"{PATH.DATA}/{DATASET_FOLDER}/{dataset_directory}/{dataset_file}"):
            continue
        # for each file in dataset
        blob_client = SERVICE_STORAGE.blob_service_client.get_blob_client(
            container=f"{organizarion_id_lower}",
            blob=f"{workspace_id_lower}/datasets/{dataset_id_id_lower}/{dataset_file}"
        )
        with open(f"{PATH.DATA}/{DATASET_FOLDER}/{dataset_directory}/{dataset_file}", "rb") as data:
            blob_client.upload_blob(data)

def upload_lever_file(scenario, dataset_id, file_name):

    # path blob name
    organizarion_id_lower = str(SERVICES.organization.get('id')).lower()
    workspace_id_lower = str(SERVICES.workspace.get('id')).lower()
    dataset_id_id_lower = str(dataset_id).lower()

    # create is not exists
    create_container_upsert(organizarion_id_lower)

    if os.path.isdir(f"{PATH.DATA}/{SCENARIO_FOLDER}/{scenario.get(NAME)}/{MASS_LEVER_EXCEL_FILE}"):
        # for each file in dataset
        blob_client = SERVICE_STORAGE.blob_service_client.get_blob_client(
            container=f"{organizarion_id_lower}",
            blob=f"{workspace_id_lower}/datasets/{dataset_id_id_lower}/{file_name}"
        )
        with open(f"{PATH.DATA}/{SCENARIO_FOLDER}/{scenario.get(NAME)}/{MASS_LEVER_EXCEL_FILE}/{file_name}", "rb") as data:
            blob_client.upload_blob(data)


async def upload_input_files():

    container_id_lower = str(SERVICE_STORAGE.container_dataset).lower()
    container_client = SERVICE_STORAGE.blob_service_client.get_container_client(container_id_lower)
    
    if PATH.zip_file is None:
        await LOGGER.logger('the zip file not exist')
        await run_exit(LOGGER)
    

    blob_client = SERVICE_STORAGE.blob_service_client.get_blob_client(container_id_lower, PATH.zip_file)
    if blob_client.exists():
        container_client.delete_blob(PATH.zip_file)

    with open(f"{PATH.INPUT}/{PATH.zip_file}", "rb") as data:
        blob_client.upload_blob(data)
