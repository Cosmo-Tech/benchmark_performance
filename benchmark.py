import sys
import os
import asyncio
from utils.clean_up import clean_up_data_folder
from utils.constants import DATASET, PATH_INPUT
from utils.run_exit import run_exit
from results.get_logs import get_logs
from results.export_results import export_results_detailed
from results.export_results import export_results_global
from results.export_results import export_main_report
from results.export_results import export_report
from storage.upload_results_to_perf_account import upload_result_file, zip_results_files
from storage.generate_sas_token import generate_sas_token
from scenario.get_scenarios import get_scenarios
from scenario.create_scenario_flow import create_scenario_flow
from scenario.delete_scenario import delete_scenario
from dataset.create_dataset_flow import create_dataset_flow

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.path import Path
PATH = Path.__call__()

from utils.datasets import DatasetsList
DATASETS = DatasetsList.__call__()

from utils.services import Services
SERVICES = Services.__call__()

from utils.services_storage import ServiceStorage
SERVICE_STORAGE = ServiceStorage.__call__()

from utils.services_scenario import ServicesScenarios
RUN = ServicesScenarios.__call__()


async def get_logs_accumulated():
    scenarios = SERVICES.scenarios
    datasets = SERVICES.datasets_id
    scenarios_created = SERVICES.scenarios_created
    run_scenarios = SERVICES.run_scenarios

    for k,item in enumerate(scenarios):
        scenario = scenarios[k]
        dataset_id = datasets[k]
        scenario_id = scenarios_created[k]
        run_scenario_id = run_scenarios[k]

        await get_logs(dataset_id, scenario_id, run_scenario_id, scenario)

    await LOGGER.logger('uploading performance results to storage...')
    description_page = export_main_report()
    global_page = export_results_global()
    detail_page = export_results_detailed()
    export_report(description_page, global_page, detail_page)

    zip_results_files()
    run_test_id = await upload_result_file()
    await generate_sas_token(run_test_id)


async def check_dataset_for_created(dataset):
    if not dataset.get(PATH_INPUT):
        await LOGGER.logger("there is no path input for your dataset")
        await run_exit(LOGGER)
    return await create_dataset_flow(dataset)

async def run_main_flow(scenario):
    
    # retrieve dataset
    dataset = await DATASETS.__get_by_name__(scenario.get(DATASET))
    if dataset is None:
        dataset = await SERVICES.__get_dataset_by_name__(scenario.get(DATASET))
        if dataset.get('id') is None:
            await LOGGER.logger("creating new dataset")
            dataset = await check_dataset_for_created(dataset)

    # Create scenario
    scenario_created_id = await create_scenario_flow(scenario, dataset)

    # collecting data
    await RUN.set_scenarios(scenario_created_id)
    SERVICES.set_scenarios(scenario)
    SERVICES.set_scenario_created(scenario_created_id)
    SERVICES.set_datasets_id(dataset.get('id'))


async def main():
    # get global keys
    scenarios = await get_scenarios()

    # iteration scenarios
    for scenario in scenarios:
        # replace_run_template(services_object, scenario_object.compute_size)
        await run_main_flow(scenario)

    run_scenarios = await RUN.run_scenario_async()
    SERVICES.set_run_scenarios(run_scenarios)

    await get_logs_accumulated()

if __name__ == '__main__':
    HOME = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    PATH.__set_path__(HOME)
    clean_up_data_folder()
    asyncio.run(main())
