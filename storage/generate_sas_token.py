""".env"""
import sys
from datetime import date
from datetime import datetime, timedelta
from decouple import config
from azure.storage.blob import generate_blob_sas, BlobSasPermissions

CONTAINER_NAME_RESULTS = "performance-results"
SUMMARY_ZIP_NAME = "results-summary.zip"

def generate_sas_token(services: object, run_test_id: str):
    """Generate sas token to shared your results"""
    account_name = config('ACCOUNT_NAME')
    account_key = config('ACCOUNT_KEY')
    if account_name and account_key:
        container_name=CONTAINER_NAME_RESULTS

        organizarion_id_lower = str(services.organization.id).lower()
        workspace_id_lower = str(services.workspace.id).lower()
        file_to_download = SUMMARY_ZIP_NAME
        blob_name=f"{organizarion_id_lower}/{workspace_id_lower}/results/{date.today().isoformat()}/{run_test_id}/{file_to_download}"

        blob_permission = BlobSasPermissions(read=True)

        url = generate_blob_sas(
            account_name=account_name,
            container_name=container_name,
            blob_name=blob_name,
            account_key=account_key,
            expiry=datetime.utcnow() + timedelta(days=365),
            permission=blob_permission
        )

        print(f'https://{account_name}.blob.core.windows.net/{CONTAINER_NAME_RESULTS}/{blob_name}?{url}')
    else:
        print("check your .env file")
        sys.exit(1)
