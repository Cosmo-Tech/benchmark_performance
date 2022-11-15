""".env"""
import os
import uuid
from zipfile import ZipFile
from datetime import date
from decouple import config
from azure.storage.blob import BlobServiceClient

CONTAINER_NAME_RESULTS = "performance-results"
SUMMARY_ZIP_NAME = "results-summary.zip"

def upload_result_file(services:object) -> str:
    """upoload results files to storage container performance-results"""
    connection_string = config('CONNECTION_STRING')
    # blob connection client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    run_test_id = str(uuid.uuid4())
    print("run test id: ", run_test_id)
    file_to_upload = SUMMARY_ZIP_NAME

    # Create a blob client using the local file name as the name for the blob
    organizarion_id_lower = str(services.organization_id).lower()
    workspace_id_lower = str(services.workspace_id).lower()

    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME_RESULTS,
        blob=f"{organizarion_id_lower}/{workspace_id_lower}/results/{date.today().isoformat()}/{run_test_id}/{file_to_upload}"
    )
    with open(f"./summary/{file_to_upload}", "rb") as data:
        blob_client.upload_blob(data)

    return run_test_id


def zip_results_files():
    """.env"""
    with ZipFile(f'./summary/{SUMMARY_ZIP_NAME}', 'w') as myzip:
        for file in os.listdir("./logs"):
            myzip.write(f"./logs/{file}")
