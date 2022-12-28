""".env"""
import os
import codecs
import time
from pprint import pprint
import pandas as pd
from cosmotech_api import ApiException
from cosmotech_api.api import scenario_api
from cosmotech_api.api import scenariorun_api
from results.get_info_from_logs import get_info_from_logs
from utils.constants import COMPUTE_SIZE, NAME, PERFORMANCE_TEST_CSV, SIZE
from utils.run_exit import run_exit

from utils.path import Path
PATH = Path.__call__()

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.validation_config_file import Services
SERVICES = Services.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()

async def get_status_logs(
        scenario_run_api_instance,
        scenariorun_id,
        scenario_name,
        max_start_latence,
        scenario_id,
        cpu,
        size,
        failed = False
    ):
    try:
        logs_response = scenario_run_api_instance.get_scenario_run_cumulated_logs(
            SERVICES.organization.get('id'),
            scenariorun_id
        )
        if not failed:
            await get_info_from_logs(
                str(logs_response),
                scenario_name,
                max_start_latence,
                scenario_id,
                cpu,
                size
            )
        with codecs.open(f"{PATH.LOGS}/scenariorun-logs-{scenario_name}.txt", 'w', encoding='utf-8') as file:
            pprint(logs_response, file)
    except ApiException as exception:
        await LOGGER.logger(f"Exception when calling ScenariorunApi->get_scenario_run_cumulated_logs: {exception}")
        await run_exit(LOGGER)

async def get_logs(dataset_id, scenario_id, scenariorun_id, scenario):
    api_client = await COSMO_API.__get_api__()
    scenario_api_instance = scenario_api.ScenarioApi(api_client)
    scenario_run_api_instance = scenariorun_api.ScenariorunApi(api_client)

    current_state = "Running"
    while True:
        try:
            scenario_from_api = scenario_api_instance.find_scenario_by_id(
                SERVICES.organization.get('id'),
                SERVICES.workspace.get('id'),
                scenario_id
            )
            scenario_state = str(scenario_from_api.state)
            if scenario_state != current_state:
                current_state = scenario_state
            await LOGGER.logger(f"[... state: {scenario_state} ...]")
            if (current_state in [
                    "Successful",
                    "Failed",
                    "DataIngestionFailure"
                ]):
                break
            time.sleep(30)
        except ApiException as exception:
            await LOGGER.logger(f"Exception when calling ScenarioApi->find_scenario_by_id: {exception}")
            await get_status_logs(
                scenario_run_api_instance,
                scenariorun_id,
                str(scenario.get(NAME)),
                0.0,
                str(scenario.get(COMPUTE_SIZE)),
                str(scenario.get(SIZE)),
                True
            )

    if current_state == "Successful":
        await LOGGER.logger(f"[... state: {current_state} ...]")
        # get the status for the ScenarioRun
        try:
            api_response = scenario_run_api_instance.get_scenario_run_status(
                SERVICES.organization.get('id'),
                scenariorun_id
            )
        except ApiException as exception:
            await LOGGER.logger(f"Exception when calling ScenariorunApi->get_scenario_run_status: {exception}")
            await get_status_logs(
                scenario_run_api_instance,
                scenariorun_id,
                str(scenario.get(NAME)),
                0.0,
                str(scenario.get(COMPUTE_SIZE)),
                str(scenario.get(SIZE)),
                True
            )

        data = [[
            str(scenario.get(NAME)),
            node.container_name,
            pd.to_datetime(node.start_time),
            pd.to_datetime(node.end_time),
        ] for node in api_response.nodes]

        df_log = pd.DataFrame(
                data=data,
                columns=[
                    'scenario_name',
                    'step',
                    'start_date',
                    'end_date'
                ])

        df_log['duration'] = df_log['end_date'] - df_log['start_date']
        df_log['duration(s)'] = (df_log['end_date'] - df_log['start_date']).dt.total_seconds()

        last_start = df_log['start_date'].max()
        first_start = df_log['start_date'].min()
        first_start = pd.to_datetime(df_log['start_date'].min())
        last_end_date = df_log['end_date'].max()

        df_log['latence_steps'] = (df_log['end_date']).apply(lambda x: last_start if x < last_start else x )
        df_log['latence_steps'] = (df_log['latence_steps'] - df_log['end_date']).dt.total_seconds()
        df_log['latence_steps'] = (df_log['latence_steps']).apply(lambda x: x if x else 0)

        df_log['start_latence'] = (df_log['start_date'] -pd.to_datetime(first_start)).dt.total_seconds()
        df_log['latence_temp'] = df_log['latence_steps']

        df_log['diff_end_date_and_last_start'] = (df_log['end_date']).apply(lambda y: (last_end_date - y) if y >= last_start else (y-y))
        df_log['diff_end_date_and_last_start'] = df_log['diff_end_date_and_last_start'].dt.total_seconds()
        df_log = df_log.sort_values(by=['end_date'])
        df_log = df_log.reset_index(drop=True)

        n_temp = []
        for i, _v in df_log['latence_steps'].items():
            if i >= 1:
                latence_temp = df_log['latence_steps'].iloc[i-1] - df_log['latence_steps'].iloc[i]
                n_temp.append(latence_temp)

        n_temp.append(0)

        df_log['latence_steps'] = pd.Series(n_temp)
        df_log['total_latence'] = df_log['latence_steps'] + df_log['diff_end_date_and_last_start']
        # df_log['dataset_id'] = dataset_id
        df_log['scenario_id'] = scenario_id
        df_log['cpu'] = scenario.get(COMPUTE_SIZE)
        df_log['size'] = scenario.get(SIZE)

        max_start_latence = df_log['start_latence'].max()
        df_log = df_log[
            [
                'scenario_name',
                'step',
                'start_date',
                'end_date',
                'duration(s)',
                'start_latence',
                'scenario_id',
                'cpu',
                'size'
            ]
        ]

        # write performance indicators to a local csv
        log_path = f"{PATH.LOGS}/{PERFORMANCE_TEST_CSV}"
        write_headers = False if os.path.isfile(log_path) else True
        await LOGGER.logger('[...Exporting performance results...]')
        df_log.to_csv(log_path, mode='a', header=write_headers, index=False)
        await get_status_logs(
                scenario_run_api_instance,
                scenariorun_id,
                str(scenario.get(NAME)),
                max_start_latence,
                scenario_id,
                str(scenario.get(COMPUTE_SIZE)),
                str(scenario.get(SIZE))
            )
    else:
        await LOGGER.logger(f"[{current_state}]")
        await get_status_logs(
                scenario_run_api_instance,
                scenariorun_id,
                str(scenario.get(NAME)),
                0.0,
                str(scenario.get(COMPUTE_SIZE)),
                str(scenario.get(SIZE)),
                True
            )
