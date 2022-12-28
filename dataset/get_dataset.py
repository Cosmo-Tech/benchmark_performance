from cosmotech_api import ApiException
from cosmotech_api.models import DatasetSearch
from utils.cosmo_api import CosmoClientApi
from utils.run_exit import run_exit

from cosmotech_api.api import dataset_api
COSMO_API = CosmoClientApi.__call__()

from utils.services import Services
SERVICES = Services.__call__()

from utils.datasets import DatasetsList
DATASETS = DatasetsList.__call__()

from utils.logger import Logger
LOGGER = Logger.__call__()

async def get_datasets_by_tags(tags):

    api_client = await COSMO_API.__get_api__()
    dataset_api_instance = dataset_api.DatasetApi(api_client)
    search = DatasetSearch(tags)
    try: 
        datasets = dataset_api_instance.search_datasets(SERVICES.organization.get('id'), search)
        datasets_list = [ { 'id': d.id, 'name': d.name} for d in datasets ]
    except ApiException as exc:
        await LOGGER.logger(f"Exception search datasets, {exc}")
        await run_exit(LOGGER)
    else:
        return await DATASETS.__set_datasets__(datasets_list)

