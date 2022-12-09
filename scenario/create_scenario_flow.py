""".env"""
import os
import json
import glob
from time import sleep
from cosmotech_api import ApiException
from cosmotech_api.api import scenario_api
from cosmotech_api.model import scenario
from cosmotech_api.model import scenario_run_template_parameter_value
from utils.logger import Logger

logger = Logger.__call__()

def get_scenario_description(services, path_input: str):
    """get scenario description from json file"""
    # opening json file
    file_name = glob.glob(os.path.join(f"{services.paths.data}/{path_input}/","*.json"))[0]
    scenario_description = open(f"{file_name}", 'r', encoding='UTF-8')
    return json.load(scenario_description)

def build_scenario_object(
        services: object,
        scenario_data: object,
        scenario_name: str,
        dataset_id: str
    ):
    """build scenario object with parameters values and run_template_id"""
    # get information from json scenario
    run_template_id = scenario_data.get('runTemplateId')
    # replace_run_template(services, run_template_id)
    # sleep(4)
    parameters_values = build_parameter_values(
        scenario_data.get('parametersValues'),
        scenario_name
    )

    scenario_object = scenario.Scenario(
        name = scenario_name,
        run_template_id = run_template_id,
        dataset_list = [ dataset_id ],
        parameters_values = parameters_values,
    )
    return scenario_object

def build_parameter_values(parameters_values: object, scenario_name: str):
    """build parameters values"""
    mass_lever_id = "mass_lever_excel_file"
    final_list = []
    for item in parameters_values:
        if item.get('parameterId') != str(mass_lever_id):
            final_list.append(
                scenario_run_template_parameter_value.ScenarioRunTemplateParameterValue(
                    parameter_id=str(item.get('parameterId')),
                    value=str(item.get('value'))
            ))
        else:
            if item.get('parameterId') == str("scenario_name"):
                final_list.append(
                    scenario_run_template_parameter_value.ScenarioRunTemplateParameterValue(
                        parameter_id=str(item.get('parameterId')),
                        value=str(scenario_name)
                ))
    return final_list

async def create_scenario_http_request(scenario_api_instance, services, scenario_object):
    """create scenario request to cosmotech api"""
    try:
        scenario_created = scenario_api_instance.create_scenario(
            services.organization.id,
            services.workspace.id,
            scenario_object
        )
        await logger.logger(f"scenario with id: {scenario_created.id} / {scenario_created.state} {scenario_created.name}")
        return scenario_created
    except ApiException as exception:
        await logger.logger(f"Exception when calling ScenarioApi->create_scenario: {exception}")

async def create_scenario_flow(services: object, scenario_obj: object, dataset_id: str):
    """init create scenario flow: build, creation request"""
    # instance scenario api
    scenario_api_instance = scenario_api.ScenarioApi(services.api_client)

    # get scenario description
    scenario_data = get_scenario_description(services, f"{scenario_obj.dataset.path_input}")
    # create new scenario
    scenario_object = build_scenario_object(
        services,
        scenario_data,
        scenario_obj.name,
        dataset_id
    )
    scenario_created = await create_scenario_http_request(
        scenario_api_instance,
        services,
        scenario_object
    )

    return scenario_created
