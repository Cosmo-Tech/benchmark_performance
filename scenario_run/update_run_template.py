""".env"""
# from cosmotech_api import ApiException
from cosmotech_api.model import run_template
from cosmotech_api.api import solution_api

def replace_run_template(services: object, run_template_id: str, cpu: str = "basicpool"):
    """.env"""
    solution_api_instance = solution_api.SolutionApi(services.api_client)
    run_template_object = None
    parameter_groups_list = []
    if str(run_template_id).lower().strip() == "lever":
        parameter_groups_list = [
            "simulation",
            "mass_action_lever",
            "flow_management_policies",
            "model_behavior",
            "demand_plan_group",
            "transport_duration_group",
            "production_resource_opening_time_group"
        ]
    elif str(run_template_id).lower().strip() == "milpoptimization":
        parameter_groups_list = [
            "simulation",
            "mass_action_lever",
            "optimization",
            "model_behavior",
            "demand_plan_group",
            "transport_duration_group",
            "production_resource_opening_time_group"
        ]

    if cpu == "basicpool":
        run_template_object = run_template.RunTemplate(
            id=str(run_template_id),
            fetch_scenario_parameters= True,
            apply_parameters= True,
            validate_data= True,
            send_datasets_to_data_warehouse= False,
            send_input_parameters_to_data_warehouse= False,
            pre_run= True,
            post_run= False,
            parameters_json= True,
            parameter_groups= parameter_groups_list,
            stack_steps= True,
        )
    else:
        run_template_object = run_template.RunTemplate(
            id=str(run_template_id),
            compute_size= str(cpu),
            fetch_scenario_parameters= True,
            apply_parameters= True,
            validate_data= True,
            send_datasets_to_data_warehouse= False,
            send_input_parameters_to_data_warehouse= False,
            pre_run= True,
            post_run= False,
            parameters_json= True,
            parameter_groups= parameter_groups_list,
            stack_steps= True,
        )

    solution_api_instance.add_or_replace_run_templates(
        organization_id=services.organization_id,
        solution_id=services.solution_id,
        run_template=[run_template_object]
    )
    return run_template_object
