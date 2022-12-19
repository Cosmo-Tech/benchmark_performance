""".env"""
import os
import re
import pandas as pd
from utils.logger import Logger

logger = Logger.__call__()

async def get_info_from_logs(
        path_logs,
        string_to_parse: str,
        scenario_name: str,
        max_start_latence,
        scenario_id: str,
        cpu: str,
        size: str
    ):
    """get information from logs of scenario_run"""
    pick = re.findall(r'(\[.+\])\sTotal\selapsed\stime:\s(\d{1,3}\.\d{4})', string_to_parse)
    for time_elapsed in pick:
        await logger.logger(f"{time_elapsed[0]} {time_elapsed[1]}")

    data = [[ scenario_name, node[0], '', '', node[1], 0, scenario_id, cpu, size ] for node in pick]
    columns = [
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

    d_f = pd.DataFrame(data=data, columns=columns)

    n_temp = [float(max_start_latence)]
    for i, _v in d_f['duration(s)'].items():
        if i >= 1:
            latence_temp = float(d_f['duration(s)'].iloc[i-1]) + n_temp[i-1]
            if i == 5:
                latence_temp = n_temp[i-1]
            n_temp.append(latence_temp)

    d_f['start_latence'] = pd.Series(n_temp)
    write_headers = False if os.path.isfile(f"{path_logs}/performance-steps.csv") else True
    d_f.to_csv(f"{path_logs}/performance-steps.csv", mode='a', header=write_headers, index=False)
