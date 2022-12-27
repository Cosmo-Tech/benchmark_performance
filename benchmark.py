"""
    Testing Cosmotech scenario on Azure:
    - Download a zip file of customized dataset
    - Create dataset from data
    - Create scenario from dataset
    - Run scenario
    - UPload performance indicators to storage container
    - Clean up dataset created for test
    - Clean up scenario created for test
"""
import sys
import os
import asyncio
from time import sleep
from results.get_logs import get_logs
from results.export_results import export_results_detailed
from results.export_results import export_results_global
from results.export_results import export_main_report
from results.export_results import export_report
from scenario.get_scenarios import get_scenarios
from scenario.create_scenario_flow import create_scenario_flow
from scenario_run.run_scenario_flow import run_scenario_flow
from dataset.create_dataset_flow import create_dataset_flow
from storage.upload_results_to_perf_account import upload_result_file, zip_results_files
from storage.generate_sas_token import generate_sas_token
from utils.validation_config_file import clean_up_data_folder

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.path import Path
PATH = Path.__call__()

async def run_main_flow(scenario):
    # create dataset
    dataset_created_id = await create_dataset_flow(scenario)
    # Create scenario
    scenario_created = await create_scenario_flow(scenario, dataset_created_id)
    # Run scenario
    scenario_run_created = await run_scenario_flow(scenario_created.id)
    # collect and upload logs
    await get_logs(dataset_created_id, scenario_created.id, scenario_run_created.id, scenario)

async def main():
    # get global keys
    scenarios = await get_scenarios()
    # iteration scenarios
    for scenario in scenarios:
        # replace_run_template(services_object, scenario_object.compute_size)
        # await logger.logger(f"Update run_template to computeSize: {scenario_object.compute_size} ...")
        # wait update done
        # sleep(4)
        # run scenario flow
        await run_main_flow(scenario)

    # come back to basicpool
    # replace_run_template(services_object, "basicpool")

    await LOGGER.logger('Uploading performance results to storage...')
    description_page = export_main_report()
    global_page = export_results_global()
    detail_page = export_results_detailed()
    export_report(description_page, global_page, detail_page)
    sleep(1)
    zip_results_files()
    run_test_id = await upload_result_file()
    await generate_sas_token(run_test_id)

if __name__ == '__main__':
    HOME = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    PATH.__set_path__(HOME)
    # clean up data, logs and summary
    clean_up_data_folder()
    asyncio.run(main())
