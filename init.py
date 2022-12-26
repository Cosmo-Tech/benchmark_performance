"""Script to create .env and comsotest.config.yml files"""
import sys
import os

if __name__ == '__main__':
    HOME = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    ACCOUNT_NAME = sys.argv[2] if len(sys.argv) > 2 else ""
    ACCOUNT_KEY = sys.argv[3] if len(sys.argv) > 3 else ""
    CONNECTION_STRING = sys.argv[4] if len(sys.argv) > 4 else ""

    TENANT_ID = sys.argv[5] if len(sys.argv) > 5 else ""
    CLIENT_ID = sys.argv[6] if len(sys.argv) > 6 else ""
    SECRET = sys.argv[7] if len(sys.argv) > 7 else ""

    path = os.path.join(HOME, ".env")
    with open(path, 'w', encoding='utf-8') as file_env:
        ENV_SAMPLE = """ACCOUNT_NAME=%s
ACCOUNT_KEY=%s
CONNECTION_STRING=%s
""" % (ACCOUNT_NAME, ACCOUNT_KEY, CONNECTION_STRING)
        file_env.write(ENV_SAMPLE)
        print(".env file... OK")

    path = os.path.join(HOME, "cosmotest.config.yml")
    with open(path, 'w', encoding='utf-8') as file:
        CONFIG_SAMPLE = """azure:
    tenant_id: %s
    client_id: %s
    client_secret: %s
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
""" % (TENANT_ID, CLIENT_ID, SECRET)
        file.write(CONFIG_SAMPLE)
        print("cosmotest.config.yml file... OK")
