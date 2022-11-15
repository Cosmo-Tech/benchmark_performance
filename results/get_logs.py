""".env"""
import os
import sys
import codecs
import time
from pprint import pprint
import pandas as pd
from cosmotech_api import ApiException
from cosmotech_api.api import scenario_api
from cosmotech_api.api import scenariorun_api
from dataset.delete_dataset import delete_dataset_workspace
from scenario.delete_scenario import delete_scenario
from results.get_info_from_logs import get_info_from_logs
from storage.upload_results_to_perf_account import upload_result_file, zip_results_files
from storage.generate_sas_token import generate_sas_token

def get_status_logs(
        scenario_run_api_instance: object,
        services: object,
        scenariorun_id: str,
        scenario_name: str,
        max_start_latence,
        scenario_id: str,
        cpu: str,
        size: str,
        failed = False
    ):
    """get status logs of scenario_run, export to txt file"""
    try:
        logs_response = scenario_run_api_instance.get_scenario_run_cumulated_logs(
            services.organization_id,
            scenariorun_id
        )
        if not failed:
            get_info_from_logs(
                str(logs_response),
                scenario_name,
                max_start_latence,
                scenario_id,
                cpu, 
                size
            )
        with codecs.open(f"./logs/scenariorun-logs-{scenario_name}.txt", 'w', encoding='utf-8') as file:
            pprint(logs_response, file)
    except ApiException as exception:
        print(f"Exception when calling ScenariorunApi->get_scenario_run_cumulated_logs: {exception}")


def get_logs(
        services, dataset_id : str,
        scenario_id: str,
        scenariorun_id: str,
        scenario_object: object
    ):
    """main get logs from cosmotech api and build csv file"""
    scenario_api_instance = scenario_api.ScenarioApi(services.api_client)
    scenario_run_api_instance = scenariorun_api.ScenariorunApi(services.api_client)
    current_state = ''
    while True:
        try:
            scenario = scenario_api_instance.find_scenario_by_id(
                services.organization_id,
                services.workspace_id,
                scenario_id
            )
            scenario_state = str(scenario.state)
            if scenario_state != current_state:
                current_state = scenario_state
            if (scenario_state in [
                    "Successful",
                    "Failed",
                    "DataIngestionFailure"
                ]):
                break
            print(f'[... state: {current_state} ...]')
            time.sleep(60)
        except ApiException as exception:
            print(f"Exception when calling ScenarioApi->find_scenario_by_id: {exception}")

    if current_state == "Successful":
        # get the status for the ScenarioRun
        try:
            api_response = scenario_run_api_instance.get_scenario_run_status(
                services.organization_id,
                scenariorun_id
            )
        except ApiException as exception:
            print(f"Exception when calling ScenariorunApi->get_scenario_run_status: {exception}")

        data = [[
            str(scenario_object.name),
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
        df_log['cpu'] = scenario_object.compute_size
        df_log['size'] = scenario_object.size

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
        log_path = "./logs/performance-test.csv"
        write_headers = False if os.path.isfile(log_path) else True
        print('[...Exporting performance results...]')
        df_log.to_csv(log_path, mode='a', header=write_headers, index=False)
        get_status_logs(
                scenario_run_api_instance,
                services,
                scenariorun_id,
                str(scenario_object.name),
                max_start_latence,
                scenario_id,
                str(scenario_object.compute_size),
                str(scenario_object.size)
            )
        # clean up
        delete_dataset_workspace(services, scenario_object.dataset.path_input, dataset_id)
        delete_scenario(services, scenario_id)
    else:
        print("[Failed]")
        get_status_logs(
                scenario_run_api_instance,
                services,
                scenariorun_id,
                str(scenario_object.name),
                str(scenario_id),
                str(scenario_object.compute_size),
                str(scenario_object.size),
                True
            )
        # clean up
        delete_dataset_workspace(services, scenario_object.dataset.path_input, dataset_id)
        delete_scenario(services, scenario_id)
        print('Uploading performance results to storage...')
        zip_results_files()
        run_test_id = upload_result_file(services)
        generate_sas_token(services, run_test_id)
        sys.exit(1)
