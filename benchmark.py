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
import websockets
from time import sleep
from results.get_logs import get_logs
from results.export_results import export_results_detailed
from results.export_results import export_results_global
from results.export_results import export_main_report
from results.export_results import export_report
from scenario.get_scenarios import get_scenarios
from scenario.create_scenario_flow import create_scenario_flow
# from scenario.delete_scenario import delete_scenario
from scenario_run.run_scenario_flow import run_scenario_flow
from scenario_run.update_run_template import replace_run_template
from dataset.create_dataset_flow import create_dataset_flow
from storage.upload_results_to_perf_account import upload_result_file, zip_results_files
from storage.generate_sas_token import generate_sas_token
from utils.validation_config_file import Env
from utils.validation_config_file import clean_up_data_folder
from utils.validation_config_file import Services
from utils.logger import Logger
sys.dont_write_bytecode = True

logger = Logger.__call__()

async def run_main_flow(services: object, scenario_obj: object):
    """main brenchmark for each scenario: create dataset, create scenario, run scenario, get logs"""
    # create dataset
    dataset_created_id = await create_dataset_flow(services, scenario_obj)

    # Create scenario
    scenario_created = await create_scenario_flow(services, scenario_obj, dataset_created_id)

    # Run scenario
    scenario_run_created = run_scenario_flow(services, scenario_created.id)

    # collect and upload logs
    await get_logs(services, dataset_created_id, scenario_created.id, scenario_run_created.id, scenario_obj)


async def main(data_folder: str, logs_folder: str, summary_folder: str, home_folder: str):
    """main function async"""
    # clean up data, logs and summary
    clean_up_data_folder(data_folder, logs_folder, summary_folder)

    # get global keys
    api_client, organization, solution, workspace, name_file_storage, connector, connector_type, scenarios = await get_scenarios(path_data, HOME)
    if api_client is not None:
        # build services to share
        services_object = Services(
            api_client,
            organization,
            workspace,
            solution,
            {
                'id': connector.id,
                'name': connector.name,
                'url': connector.url,
                'type': connector_type,
            },
            {
                'data': data_folder,
                'logs': logs_folder,
                'summary': summary_folder
            }
        )

    # iteration scenarios
    for scenario in scenarios:
        scenario_object = Env(scenario)
        scenario_object.dataset = Env(scenario_object.dataset)

        replace_run_template(services_object, scenario_object.compute_size)
        await logger.logger(f"Update run_template to computeSize: {scenario_object.compute_size} ...")
        # wait update done
        sleep(4)
        # run scenario flow
        await run_main_flow(services_object, scenario_object)

    # come back to basicpool
    replace_run_template(services_object, "basicpool")

    await logger.logger('Uploading performance results to storage...')
    description_page = export_main_report(services_object, name_file_storage)
    global_page = export_results_global(path_logs, name_file_storage)
    detail_page = export_results_detailed(path_logs, name_file_storage)
    export_report(services_object, description_page, global_page, detail_page)
    sleep(1)
    zip_results_files(services_object)
    run_test_id = await upload_result_file(services_object)
    await generate_sas_token(services_object, run_test_id)

if __name__ == '__main__':
    HOME = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    path_data = os.path.join(HOME, "data")
    path_logs = os.path.join(HOME, "logs")
    path_summary = os.path.join(HOME, "summary")
    asyncio.run(main(path_data, path_logs, path_summary, HOME))
