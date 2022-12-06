"""Script to create .env and comsotest.config.yml files"""
import sys
import os

if __name__ == '__main__':
    HOME = sys.argv[1]
    path = os.path.join(HOME, ".env")
    with open(path, 'w', encoding='utf-8') as file_env:
        ENV_SAMPLE = """ACCOUNT_NAME=
ACCOUNT_KEY=
CONNECTION_STRING=
"""
        file_env.write(ENV_SAMPLE)
        print(".env file... OK")

    path = os.path.join(HOME, "cosmotest.config.yml")
    with open(path, 'w', encoding='utf-8') as file:
        CONFIG_SAMPLE = """azure:
    tenant_id: yout_tenant_id
    client_id: yout_client_id
    client_secret: yout_client_secret
    cosmo_api_scope: http://dev.api.cosmotech.com/.default
    cosmo_api_host: https://dev.api.cosmotech.com

cosmo_test:
    organization:
        id: O-gZYpnd27G7                                # your organization (required)
        name: Cosmo Tech                                # information only (required)
    workspace:
        id: W-QPpQ47r2L9                                # your workspace (required)
        name: Supply Chain Dev                          # information only (required)
    solution:
        id: SOL-0xAAgEvr3J                              # your solution (required)
        version: 1.0.0                                  # your solution version (required)
        name: Supply Chain Solution                     # information only (required)
    connector:
        id: c-q2859zy34wmm                              # connector AKS or ADT (required)
        name: AKS                                       # information only (required)
        url: ""                                         # # URL ADT

    name_file_storage: scenario_demo_test.zip           # blob name in your 'permformance-datasets' container
    scenarios:
        
        "1":                                                                # select a name (string required)
            name: "large basicpool"                                         # select a size (number or string required)
            size: 100000                                                    # select a name (string required)
            compute_size: "basicpool"                                       # 'basicpool' or 'highcpu'
            dataset:
                name: "performance large size basicpool"                    # select a name
                path_input: "scenario_a"                                    # folder's name in scenario_demo_test.zip

        "2":                                            
            name: "medium highcpu"
            size: 10000
            compute_size: "highcpu"
            dataset:
                name: "performance large size highcpu"
                path_input: "scenario_a"
"""
        file.write(CONFIG_SAMPLE)
        print("cosmotest.config.yml file... OK")
