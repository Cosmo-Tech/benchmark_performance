""".env"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def export_results(filename_zip: str):
    """option 1 to results export a pdf"""
    offset_end=50
    interval=20
    filename_results = './logs/performance-test.csv'

    dataframe_original = pd.read_csv(f'{filename_results}')
    dataframe_original['start_date'] = pd.to_datetime(dataframe_original['start_date'])
    scenario_list = dataframe_original.groupby(['scenario_id'])

    original_df_steps = pd.read_csv('./logs/performance-steps.csv')
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
    fig, a_x = plt.subplots(1, constrained_layout=True, figsize=(20,11))
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

    fig.savefig('./logs/scenario_results.pdf', bbox_inches='tight')


def export_results_option_2(filename_zip: str):
    """option 2 to results export a pdf"""
    colors = "salmon teal cyan r b g yellow black".split(' ')
    offset_end=20
    interval=20
    filename_results = './logs/performance-test.csv'

    dataframe_original = pd.read_csv(f'{filename_results}')
    dataframe_original['start_date'] = pd.to_datetime(dataframe_original['start_date'])
    scenario_list = dataframe_original.groupby(['scenario_id'])

    original_df_steps = pd.read_csv('./logs/performance-steps.csv')
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

    x_max = max(max_list) + offset_end

    fig, a_x = plt.subplots(len(data), 1, constrained_layout=True, figsize=(20,12))
    fig.suptitle(f'Results run test {filename_zip}', fontsize=11)
    for i, graph in enumerate(data):
        a_x[i].set_xlabel('Duration (s)')
        a_x[i].set_xlim(left=0, right=x_max)
        a_x[i].grid('on', which='major', axis='x' )
        a_x[i].grid('on', which='major', axis='y' )
        a_x[i].set_xticks(np.arange(0, x_max, interval))

        data = a_x[i].barh(graph['step'], graph['duration(s)'], left=graph['start_latence'], height=0.8, label=graph['scenario_name'].iloc[0], color=colors[i])
        a_x[i].bar_label(data, labels=graph['duration(s)'], padding=3)
        a_x[i].legend()

    fig.tight_layout(pad=2.0)

    fig.savefig('./logs/scenario_results_option2.pdf', bbox_inches='tight')


def export_results_option_3(filename_zip: str):
    """option 3 to results export a pdf"""
    offset_end=50
    interval=20
    filename_results = './logs/performance-test.csv'

    dataframe_original = pd.read_csv(f'{filename_results}')
    dataframe_original['start_date'] = pd.to_datetime(dataframe_original['start_date'])
    # scenario_list = dataframe_original.groupby(['scenario_name'])

    original_df_steps = pd.read_csv('./logs/performance-steps.csv')
    original_df_steps['start_date'] = pd.to_datetime(original_df_steps['start_date'])

    dataframe_original = pd.concat([dataframe_original, original_df_steps])

    dataframe_original['step'] = (dataframe_original['step']).apply(lambda y: '[Run/Engine]' if y.startswith('[Run/Engine]') else y) + (dataframe_original['scenario_name']).apply(lambda x: f' [{str(x)}] ')
    dataframe_original['step'] = (dataframe_original['step']).apply(lambda y: y.replace('Container-1', ''))


    dataframe_original = dataframe_original[dataframe_original["step"].str.startswith('[Run/Engine]')]
    x_max = dataframe_original['duration(s)'].max() + dataframe_original['start_latence'].max() + offset_end
    dataframe_original['total'] =  dataframe_original['duration(s)'] + dataframe_original['start_latence']

    fig, a_x = plt.subplots(1, constrained_layout=True, figsize=(20,2))
    fig.suptitle(f'Total {filename_zip}', fontsize=11)
    a_x.set_xlabel('Duration (s)')
    a_x.set_xlim(left=0, right=x_max)
    a_x.grid('on', which='major', axis='x' )
    a_x.grid('on', which='major', axis='y' )
    a_x.set_xticks(np.arange(0, x_max, interval))

    graph = a_x.barh(dataframe_original['step'], dataframe_original['total'], height=0.8)
    a_x.bar_label(graph, labels=dataframe_original['total'], padding=3)

    fig.savefig('./logs/scenario_results_option3.pdf', bbox_inches='tight')
