import os
import json
import glob
from cosmotech_api import ApiException
from cosmotech_api.api import scenario_api
from cosmotech_api.model import scenario
from cosmotech_api.model import scenario_run_template_parameter_value
from dataset.create_dataset_lever import create_dataset_lever_flow
from utils.run_exit import run_exit
from utils.constants import MASS_LEVER_EXCEL_FILE, NAME, SCENARIO_FOLDER

from utils.path import Path
PATH = Path.__call__()

from utils.logger import Logger
LOGGER = Logger.__call__()

from utils.validation_config_file import Services
SERVICES = Services.__call__()

from utils.cosmo_api import CosmoClientApi
COSMO_API = CosmoClientApi.__call__()

def get_scenario_description_json(scenario_name):
    # opening json file
    file_name = glob.glob(os.path.join(f"{PATH.DATA}/{SCENARIO_FOLDER}/{scenario_name}","*.json"))
    file_name = file_name[0] if len(file_name) > 0 else None
    if file_name is None:
        return None

    scenario_description = open(f"{file_name}", 'r', encoding='UTF-8')
    return json.load(scenario_description)

def build_scenario_object(scenario_data, scenario_name, dataset_id, mass_lever_id):
    # get information from json scenario
    run_template_id = scenario_data.get('runTemplateId')
    parameters_values = scenario_data.get('parametersValues')
    parameters_values = list(map(update_mass_lever, parameters_values, [{ 'value': mass_lever_id} for i in range(len(parameters_values))]))
    parameters = build_parameter_values(parameters_values, scenario_name)

    scenario_object = scenario.Scenario(
        name = scenario_name,
        run_template_id = run_template_id,
        dataset_list = [ dataset_id ],
        parameters_values = parameters,
    )
    return scenario_object

def build_parameter_values(parameters_values, scenario_name):
    final_list = []
    for item in parameters_values:
        if item.get('parameterId') == str("scenario_name"):
            final_list.append(
                scenario_run_template_parameter_value.ScenarioRunTemplateParameterValue(
                    parameter_id=str(item.get('parameterId')),
                    value=str(scenario_name),
            ))
        else:
            final_list.append(
                scenario_run_template_parameter_value.ScenarioRunTemplateParameterValue(
                    parameter_id=str(item.get('parameterId')),
                    value=str(item.get('value'))
            ))
            
    return final_list

async def create_scenario_http_request(scenario_api_instance, scenario_object):
    try:
        scenario_created = scenario_api_instance.create_scenario(
            SERVICES.organization.get('id'),
            SERVICES.workspace.get('id'),
            scenario_object
        )
        await LOGGER.logger(f"scenario with id: {scenario_created.id} / {scenario_created.state} {scenario_created.name}")
        return scenario_created
    except ApiException as exception:
        await LOGGER.logger(f"Exception when calling ScenarioApi->create_scenario: {exception}")

def get_scenario_description_mass_lever(path_input):
    # opening json file
    file_name = glob.glob(os.path.join(f"{PATH.DATA}/{SCENARIO_FOLDER}/{path_input}/{MASS_LEVER_EXCEL_FILE}","*.xlsx"))
    file_name = file_name[0] if len(file_name) > 0 else None
    return file_name

def update_mass_lever(item, item2):
    if item.get('varType') == "%DATASETID%" and item.get('parameterId') == MASS_LEVER_EXCEL_FILE:
        item.update(item2)
    return item

async def create_scenario_flow(scenario, dataset):
    # instance scenario api
    api_client = await COSMO_API.__get_api__()
    scenario_api_instance = scenario_api.ScenarioApi(api_client)

    # get scenario description
    scenario_data = get_scenario_description_json(scenario.get(NAME))
    if scenario_data is None:
        await LOGGER.logger("no scenario.json file")
        await run_exit(LOGGER)

    mass_lever = get_scenario_description_mass_lever(scenario.get(NAME))
    if mass_lever is None:
        await LOGGER.logger("no mass lever excel file")
        await run_exit(LOGGER)
    mass_lever_id = await create_dataset_lever_flow(scenario, os.path.basename(mass_lever))

    # create new scenario
    scenario_object = build_scenario_object(scenario_data, scenario.get(NAME), dataset.get('id'), mass_lever_id)
    scenario_created = await create_scenario_http_request(
        scenario_api_instance,
        scenario_object
    )

    return scenario_created.id
