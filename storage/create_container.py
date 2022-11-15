""".env"""
import sys
from decouple import config
from azure.storage.blob import BlobServiceClient

def create_container_upsert(container_name: str):
    """.env"""
    connection_string = config('CONNECTION_STRING')
    if connection_string:
        # blob connection client
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Get the container logs
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            blob_service_client.create_container(container_name)
            print(f'{container_name} creation... OK')
    else:
        print("Error: CONNECTION_STRING empty in .env")
        sys.exit(1)
