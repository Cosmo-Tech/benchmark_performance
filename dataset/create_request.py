from cosmotech_api import ApiException

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.validation_config_file import Services
SERVICES = Services.__call__()

async def create_dataset_http_request(dataset_api_instance, dataset_object):
    try:
        dataset_created = dataset_api_instance.create_dataset(SERVICES.organization.get('id'), dataset_object)
        await LOGGER.logger(f"dataset with id  {dataset_created.id} created")
        return dataset_created
    except ApiException as exception:
        await LOGGER.logger(f"Exception when calling DatasetApi->create_dataset: {exception}")
        return None