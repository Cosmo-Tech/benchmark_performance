"""Script to create .env and comsotest.config.yml files"""
import sys
import os

if __name__ == '__main__':
    HOME = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
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
        id: O-gZYpnd27G7
        name: Cosmo Tech
    workspace:
        id: W-QPpQ47r2L9
        name: Supply Chain Dev
    solution:
        id: SOL-0xAAgEvr3J
        version: 1.0.0
        name: Supply Chain Solution
    connector:
        id: c-q2859zy34wmm
        name: AKS
        url: ""

    name_file_storage: scenario_demo_test.zip
    scenarios:

        "1":
            name: "large basicpool"
            size: 100000k
            compute_size: "basicpool"
            dataset:
                name: "performance large size basicpool"
                path_input: "scenario_a"

        "2":                
            name: "medium basicpool"
            size: 10000k
            compute_size: "basicpool"
            dataset:
                name: "performance medium size basicpool"
                path_input: "scenario_b"
"""
        file.write(CONFIG_SAMPLE)
        print("cosmotest.config.yml file... OK")
