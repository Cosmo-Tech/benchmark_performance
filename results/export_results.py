""".env"""
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def export_results(path_logs, filename_zip: str):
    """option 1 to results export a pdf"""
    offset_end=50
    interval=20
    filename_results = f'{path_logs}/performance-test.csv'

    dataframe_original = pd.read_csv(f'{filename_results}')
    dataframe_original['start_date'] = pd.to_datetime(dataframe_original['start_date'])
    scenario_list = dataframe_original.groupby(['scenario_id'])

    original_df_steps = pd.read_csv(f'{path_logs}/performance-steps.csv')
    original_df_steps['start_date'] = pd.to_datetime(original_df_steps['start_date'])

    dataframe_original = pd.concat([dataframe_original, original_df_steps])
    dataframe_original['step'] = (dataframe_original['step']).apply(lambda y: 'workflow' if y.startswith('workflow') else y) + (dataframe_original['scenario_id']).apply(lambda x: f' [{str(x)}] ')
    dataframe_original['step'] = (dataframe_original['step']).apply(lambda y: y.replace('Container-1', '').replace('Container', ''))

    # scenario list
    scenario_list = list(scenario_list.groups.keys())

    data = []
    for scenario in scenario_list:
        data.append(dataframe_original[dataframe_original['scenario_id'] == str(scenario)])

    max_list = []
    for item in data:
        max_list.append(item['duration(s)'].iloc[len(item['step'])-1].max() + item['start_latence'].iloc[len(item['step'])-1].max())

    x_max = max(max_list) + offset_end
    fig_size = 20 if len(data) >= 4 else 11
    fig, a_x = plt.subplots(1, constrained_layout=True, figsize=(20,fig_size))
    fig.suptitle(f'Result run test {filename_zip}', fontsize=11)
    a_x.set_xlabel('Duration (s)')
    a_x.set_xlim(left=0, right=x_max)
    a_x.grid('on', which='major', axis='x' )
    a_x.grid('on', which='major', axis='y' )
    a_x.set_xticks(np.arange(0, x_max, interval))

    for item in data:
        data = a_x.barh(item['step'], item['duration(s)'], left=item['start_latence'], height=0.8, label=item['scenario_name'].iloc[0])
        a_x.bar_label(data, labels=item['duration(s)'], padding=3)

    a_x.legend()
    fig.tight_layout(pad=2.0)

    fig.savefig(f'{path_logs}/scenario_results.pdf', bbox_inches='tight')


def export_results_detailed(path_logs, filename_zip: str):
    """option 2 to results export a pdf"""
    colors = "salmon teal cyan r b g yellow black".split(' ')
    dataframe_original = pd.read_csv(f'{path_logs}/performance-test.csv')
    dataframe_original['start_date'] = pd.to_datetime(dataframe_original['start_date'])
    scenario_list = dataframe_original.groupby(['scenario_id'])

    original_df_steps = pd.read_csv(f'{path_logs}/performance-steps.csv')
    original_df_steps['start_date'] = pd.to_datetime(original_df_steps['start_date'])

    dataframe_original = pd.concat([dataframe_original, original_df_steps])
    dataframe_original['step'] = (dataframe_original['step']).apply(lambda y: 'workflow' if y.startswith('workflow') else y)
    dataframe_original['step'] = (dataframe_original['step']).apply(lambda y: y.replace('Container-1', ''))

    # scenario list
    scenario_list = list(scenario_list.groups.keys())
    data = []
    for scenario in scenario_list:
        data.append(dataframe_original[dataframe_original['scenario_id'] == str(scenario)])

        max_list = []
    for item in data:
        max_list.append(item['duration(s)'].iloc[len(item['step'])-1].max() + item['start_latence'].iloc[len(item['step'])-1].max())

    x_max = max(max_list) + 20

    if len(data) > 1:
        fig_size = 20 if len(data) >= 4 else 11
        fig, a_x = plt.subplots(len(data), 1, constrained_layout=True, figsize=(20,fig_size))
        fig.suptitle(f'Results run test {filename_zip}', fontsize=11)
        for i, graph in enumerate(data):
            a_x[i].set_xlabel('Duration (s)')
            a_x[i].set_xlim(left=0, right=x_max)
            a_x[i].grid('on', which='major', axis='x' )
            a_x[i].grid('on', which='major', axis='y' )
            a_x[i].set_xticks(np.arange(0, x_max, 20))

            data = a_x[i].barh(graph['step'], graph['duration(s)'], left=graph['start_latence'], height=0.8, label=graph['scenario_name'].iloc[0], color=colors[i])
            a_x[i].bar_label(data, labels=graph['duration(s)'], padding=3)
            a_x[i].legend()
    else:
        fig, a_x = plt.subplots(1, constrained_layout=True, figsize=(20,11))
        fig.suptitle(f'Detailed Execution time by step {filename_zip}', fontsize=11)
        a_x.set_xlabel('Execution time (s)')
        a_x.set_xlim(left=0, right=x_max)
        a_x.grid('on', which='major', axis='x' )
        a_x.grid('on', which='major', axis='y' )
        a_x.set_xticks(np.arange(0, x_max, 20))

        graph = a_x.barh(data[0]['step'], data[0]['duration(s)'], left=data[0]['start_latence'], height=0.8, label=data[0]['scenario_name'].iloc[0], color=colors[0])
        a_x.bar_label(graph, labels=data[0]['duration(s)'], padding=3)
        a_x.legend()

    fig.tight_layout(pad=2.0)
    fig.savefig(f'{path_logs}/scenario_results_detailed.pdf', bbox_inches='tight')


def export_results_global(path_logs, filename_zip: str):
    """option 3 to results export a pdf"""
    offset_end=50
    interval=20
    filename_results = f'{path_logs}/performance-test.csv'

    dataframe_original = pd.read_csv(f'{filename_results}')
    dataframe_original['start_date'] = pd.to_datetime(dataframe_original['start_date'])
    # scenario_list = dataframe_original.groupby(['scenario_name'])

    original_df_steps = pd.read_csv(f'{path_logs}/performance-steps.csv')
    original_df_steps['start_date'] = pd.to_datetime(original_df_steps['start_date'])

    dataframe_original = pd.concat([dataframe_original, original_df_steps])

    dataframe_original['step'] = (dataframe_original['step']).apply(lambda y: '[Run/Engine]' if y.startswith('[Run/Engine]') else y) + (dataframe_original['scenario_name']).apply(lambda x: f' [{str(x)}] ')
    dataframe_original['step'] = (dataframe_original['step']).apply(lambda y: y.replace('Container-1', ''))


    dataframe_original = dataframe_original[dataframe_original["step"].str.startswith('[Run/Engine]')]
    x_max = dataframe_original['duration(s)'].max() + dataframe_original['start_latence'].max() + offset_end
    dataframe_original['total'] =  round(dataframe_original['duration(s)'] + dataframe_original['start_latence'], 2)

    fig_size = 5 if len(dataframe_original['step']) >= 4 else 2
    fig, a_x = plt.subplots(1, constrained_layout=True, figsize=(20,fig_size))
    fig.suptitle(f'Total Execution time + latence, {filename_zip}', fontsize=11)
    a_x.set_xlabel('Execution time (s)')
    a_x.set_xlim(left=0, right=x_max)
    a_x.grid('on', which='major', axis='x' )
    a_x.grid('on', which='major', axis='y' )
    a_x.set_xticks(np.arange(0, x_max, interval))

    graph = a_x.barh(dataframe_original['step'], dataframe_original['total'], height=0.8)
    a_x.bar_label(graph, labels=dataframe_original['total'], padding=3)

    fig.savefig(f'{path_logs}/scenario_results_global.pdf', bbox_inches='tight')


def export_main_report(services_object, filename_zip: str):
    """Main report"""
    path_logs = services_object.paths.logs
    dataframe_original = pd.read_csv(f'{path_logs}/performance-test.csv')
    dataframe_original['start_date'] = pd.to_datetime(dataframe_original['start_date'])

    # List scenario names
    # scenario_name_list = list(dataframe_original.groupby(['scenario_name']).groups.keys())
    scenario_list = list(dataframe_original.groupby(['cpu']).groups.keys())

    result_by_cpu = []
    data = []
    for cpu in scenario_list:
        data.append(dataframe_original[dataframe_original['cpu'] == str(cpu)])


    fig, axs = plt.subplots(3,1, figsize=(15,15))
    fig.suptitle(f'Result performance test {filename_zip}', fontsize=11)
    plt.subplots_adjust(wspace=0.6, hspace=0.5)
    #################################################
    for item in data:
        max_list = []
        size_list = []
        scenario_id_list = list(item.groupby(['scenario_id']).groups.keys())

        new_data = []
        for scenario in scenario_id_list:
            new_data.append(item[item['scenario_id'] == str(scenario)])

        for sub_item in new_data:
            max_list.append(sub_item['duration(s)'].iloc[len(sub_item['step'])-1].max() + sub_item['start_latence'].iloc[len(sub_item['step'])-1].max())
            size_list.append(f"{sub_item['size'].iloc[0]}")

        result = {}
        for i,duration in enumerate(max_list):
            result.update({ size_list[i]: duration})

        result = { k: v for k, v in sorted(result.items(), key=lambda item: item[1]) }
        result_by_cpu.append(result)
        result_x = np.array(list(result.keys()))
        result_y = np.array(list(result.values()))

        axs[1].grid('on', which='major', axis='x' )
        axs[1].grid('on', which='major', axis='y' )
        axs[1].set(xlabel='Dataset size', ylabel='Execution time (s)')
        axs[1].plot(result_x, result_y, label=item['cpu'].iloc[0])
        axs[1].legend()
    ###############################################
    axs[0].set_axis_off()
    interline = 0.05
    now = datetime.now()
    summary_headers = {
        "Date of test execution": f': {now.strftime("%D, %H:%M:%S")}',
        "Scenario summary": f": {filename_zip}",
        "Platform and component version": ": ",
        "Environement": {
            "Workspace": f": {str(services_object.workspace.name)} ({services_object.workspace.id})",
            "Solution": f": {str(services_object.solution.name)} ({services_object.solution.id})",
            "Connector": f": {str(services_object.connector.name)} ({services_object.workspace.id})",
            "Url": f": {str(services_object.connector.url)}" if services_object.connector.url is not None else ": Empty",
        },
        "Solution": {
            "Version": f": {services_object.solution.version}",
            "Name": f": {services_object.solution.name}",
            "Number of dataset": f": {str(len(scenario_id_list))}",
            "Dataset size": ": "+", ".join(size_list),
            "CPU size": ": "+", ".join(scenario_list)
        },
        "Main results/KPI's (high level)": { f'Data size: {k}' : f': {v} seconds, ({timedelta(seconds=int(v))})' for i,(k,v) in enumerate(result.items())},
    }
    margin_list = [len(w) for w in summary_headers]
    margin = max(margin_list)
    y_origin = 0
    for k, (head, valor) in enumerate(summary_headers.items()):
        x_origin = 0
        axs[0].text(x_origin, 1-y_origin-interline*(k+1), str(head), fontsize=12, weight='bold', color="salmon")
        if isinstance(valor, dict):
            offset_inner = 0.01
            x_origin = x_origin + offset_inner
            for subtitle, valor in valor.items():
                y_origin = y_origin + interline
                axs[0].text(x_origin, 1-y_origin-interline*(k+1), f'• {str(subtitle)}', fontsize=12)
                axs[0].text(x_origin+int(margin)/100-offset_inner, 1-y_origin-interline*(k+1), str(valor), fontsize=12)
        else:
            axs[0].text(x_origin+int(margin)/100, 1-y_origin-interline*(k+1), str(valor), fontsize=12, color="salmon", weight='bold')

    #################################################
    d_t = pd.DataFrame(result_by_cpu)
    d_t = d_t.transpose()
    d_t.to_csv(f"{path_logs}/performance-capacity.csv", mode='a', header=True, index=False)
    axs[2].set_axis_off()
    if len(d_t) >= 2:
        axs[2].table(
            cellText = [[ f'{val} s' for val in d_t.iloc[i]] for i,r in enumerate(d_t.index)],
            rowLabels = [f"Dataset size: {result_x[i]}" for i,r in enumerate(d_t.index)],
            colLabels = scenario_list,
            cellColours = [[ "#85BB65" if float(c) < 300.0 else "#fd9b93" for c in d_t.iloc[i]] for i,r in enumerate(d_t.index)],
            rowColours =["#FAF4D3"] * len(d_t.index),
            colColours =["#FAF4D3"] * len(d_t.index),
            cellLoc ='center',
            loc ='upper left')

    #################################################
    plt.tight_layout()

    fig.savefig(f'{path_logs}/scenario_results_report.pdf', bbox_inches='tight')
