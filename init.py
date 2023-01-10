import os
import argparse
import shutil
from storage.create_container import create_container_upsert

parser = argparse.ArgumentParser(description="Init script")
parser.add_argument('--home', action='store', default=f"{os.getcwd()}")
parser.add_argument('--account_name', action='store', default="cosmotestperf")
parser.add_argument('--account_key', action='store', default="mea8sPwvnVRFIWgLLlyBJ+V92I+fMU+XflKP1fxefVhiQQsa8pgqticlGg8gPNJ4j4lI8jFDRwYu+AStlgJOow==")
parser.add_argument('--connection_str', action='store', default="DefaultEndpointsProtocol=https;AccountName=cosmotestperf;AccountKey=mea8sPwvnVRFIWgLLlyBJ+V92I+fMU+XflKP1fxefVhiQQsa8pgqticlGg8gPNJ4j4lI8jFDRwYu+AStlgJOow==;EndpointSuffix=core.windows.net")
parser.add_argument('--tenant_id', action='store', default="e413b834-8be8-4822-a370-be619545cb49")
parser.add_argument('--client_id', action='store', default="")
parser.add_argument('--client_secret', action='store', default="")

if __name__ == '__main__':
    args = parser.parse_args()
    HOME = args.home

    if os.path.isdir(os.path.join(HOME, "input")):
        shutil.rmtree(os.path.join(HOME, "input"))
    os.mkdir(os.path.join(HOME, "input"))

    ACCOUNT_NAME = args.account_name
    ACCOUNT_KEY = args.account_key
    CONNECTION_STRING = f"DefaultEndpointsProtocol=https;AccountName={ACCOUNT_NAME};AccountKey={ACCOUNT_KEY};EndpointSuffix=core.windows.net"

    TENANT_ID = args.tenant_id
    CLIENT_ID = args.client_id
    SECRET = args.client_secret

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
  organization_id: O-gZYpnd27G7
  workspace_id: w-pr920k6lre0ym
  connector: AKS
  dataset: 
    - name: 
      path_input: 

  scenarios:

    - name: scenario test 1
      size: 100000k
      compute_size: basic
      dataset: ADT Supplychain QA

    - name: scenario test 2
      size: 100000k
      compute_size: basic
      dataset: ADT Supplychain QA

    - name: scenario test 3
      size: 100000k
      compute_size: basic
      dataset: ADT Supplychain QA

""" % (TENANT_ID, CLIENT_ID, SECRET)
        file.write(CONFIG_SAMPLE)
        print("cosmotest.config.yml file... OK")


        create_container_upsert("performance-datasets")
        create_container_upsert("performance-results")
