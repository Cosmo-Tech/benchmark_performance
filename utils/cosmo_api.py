import sys
from cosmotech_api import ApiClient
from azure.identity import ClientSecretCredential
from utils.configuration import get_configuration
from utils.singleton import SingletonType
from utils.services import Services
from utils.logger import Logger
from utils.constants import *

LOGGER = Logger.__call__()
SERVICES = Services.__call__()

class CosmoClientApi(object, metaclass=SingletonType):

    async def __get_api__(self):

        tenant_id = SERVICES.azure.get(TENANT_ID)
        client_id = SERVICES.azure.get(CLIENT_ID)
        client_secret = SERVICES.azure.get(CLIENT_SECRET)
        cosmo_api_host = SERVICES.azure.get(COSMO_API_HOST)
        cosmo_api_scope = SERVICES.azure.get(COSMO_API_SCOPE)

        dictionary = {
            TENANT_ID: tenant_id,
            CLIENT_ID: client_id,
            CLIENT_SECRET: client_secret,
            COSMO_API_SCOPE: cosmo_api_scope,
            COSMO_API_HOST: cosmo_api_host
        }
        for item in enumerate(dictionary):
            if not dictionary.get(item[1]):
                await LOGGER.logger(f'the key : {item[1]} of azure section is empty')
                sys.exit(1)

        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        token = credential.get_token(cosmo_api_scope).token
        configuration = get_configuration(cosmo_api_host, token)
        return ApiClient(configuration)