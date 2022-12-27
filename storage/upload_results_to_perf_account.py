""".env"""
import os
from os.path import basename
import uuid
from zipfile import ZipFile
from datetime import date
from decouple import config
from azure.storage.blob import BlobServiceClient

from utils.path import Path
PATH = Path.__call__()

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.validation_config_file import Services
SERVICES = Services.__call__()

CONTAINER_NAME_RESULTS = "performance-results"
SUMMARY_ZIP_NAME = "results-summary.zip"

async def upload_result_file():
    path_summary = PATH.SUMMARY
    connection_string = config('CONNECTION_STRING')
    # blob connection client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    run_test_id = str(uuid.uuid4())
    await LOGGER.logger(f"run test id: {run_test_id}")
    file_to_upload = SUMMARY_ZIP_NAME

    # Create a blob client using the local file name as the name for the blob
    organizarion_id_lower = str(SERVICES.organization.get('id')).lower()
    workspace_id_lower = str(SERVICES.workspace.get('id')).lower()

    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME_RESULTS,
        blob=f"{organizarion_id_lower}/{workspace_id_lower}/results/{date.today().isoformat()}/{run_test_id}/{file_to_upload}"
    )
    with open(f"{path_summary}/{file_to_upload}", "rb") as data:
        blob_client.upload_blob(data)

    return run_test_id

def zip_results_files():
    path_summary = PATH.SUMMARY
    path_logs = PATH.LOGS
    with ZipFile(f'{path_summary}/{SUMMARY_ZIP_NAME}', 'w') as myzip:
        for file in os.listdir(path_logs):
            myzip.write(f"{path_logs}/{file}", basename(f"{path_logs}/{file}"))
