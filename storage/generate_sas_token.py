from datetime import date
from datetime import datetime, timedelta
from decouple import config
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from utils.run_exit import run_exit
from utils.constants import ACCOUNT_KEY, ACCOUNT_NAME, CONTAINER_NAME_RESULTS, SUMMARY_ZIP_NAME
from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.validation_config_file import Services
SERVICES = Services.__call__()

async def generate_sas_token(run_test_id):
    account_name = config(ACCOUNT_NAME)
    account_key = config(ACCOUNT_KEY)
    if account_name and account_key:
        container_name=CONTAINER_NAME_RESULTS

        organizarion_id_lower = str(SERVICES.organization.get('id')).lower()
        workspace_id_lower = str(SERVICES.workspace.get('id')).lower()
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

        await LOGGER.logger(f'https://{account_name}.blob.core.windows.net/{CONTAINER_NAME_RESULTS}/{blob_name}?{url}')
    else:
        await LOGGER.logger("check your .env file")
        await run_exit(LOGGER)
