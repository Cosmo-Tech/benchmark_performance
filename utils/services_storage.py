from decouple import config
from utils.constants import ACCOUNT_KEY, ACCOUNT_NAME
from utils.constants import CONNECTION_STRING, CONTAINER_DATASET, CONTAINER_RESULT
from utils.singleton import SingletonType
from azure.storage.blob import BlobServiceClient

class ServiceStorage(object, metaclass=SingletonType):
    account_name = ""
    account_key = ""
    connection_string = ""
    container_dataset = CONTAINER_DATASET
    container_results = CONTAINER_RESULT
    blob_service_client = None
    file_name = ""

    def __init__(self):
        self.account_name = config(ACCOUNT_NAME)
        self.account_key = config(ACCOUNT_KEY)
        self.connection_string = config(CONNECTION_STRING)
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
