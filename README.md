# Benchmark performance test

Benchmark performance is a toolset to support solution to benchmark their performances.
Solution team will create their own benchmark scenarios and execute them to obtain a complete detailed overview of the platform performances.

</br>

### Requirements
- python ^3.9.2
- Account Storage
- App registration
- Benchmark input files

</br>
</br>

### Installation
---
</br>

#### Clone this project

```bash
git clone https://github.com/Cosmo-Tech/benchmark_performance.git
cd benchmark_performance
pip install -r requirements.txt
```

</br>

### Environement settings
---

#### Create ```.env``` and ```cosmotest.config.yml``` files
```bash
# python3 (linux)
python3 init.py

# python (windows)
python init.py
```
Add storage account ```🔑 Access keys``` to .env file 

#### Create your containers for your benchmark
```bash
# python3 (linux)
python3 create_containers.py

# python (windows)
python create_containers.py
```

You will see two containers in your storage account
- ```performance-datasets```
- ```performance-results```

</br>
</br>

### Create your ```Benchmark input files```
---

- Each file and folder must be gathered on a ```zip``` file and stored on your container ```performance-datasets```, with the following structure:

```bash
# benchmark_performance.zip (example)
...
├── scenario_a
│   │   ├── dataset
│   │   ├── file1.csv
│   │   ├── file2.csv
│   │   └── file3.csv
│   └── baseline.json # note 1
├── scenario_b
│   │   ├── dataset
│   │   ├── file1.csv
│   │   ├── file2.csv
│   │   └── file3.csv
│   └── baseline.json
...
```

Note 1: This is the scenario description (example)
```json
// ./scenario_a/baseline.json
{
    "runTemplateId": "Lever",
    "parametersValues": [
        {
            "parameterId": "scenario_name",
            "value": "%replaced by config file%",
            "varType": "string",
            "isInherited": false
        },
        {
            "parameterId": "start_date",
            "value": "2022-05-12T00:00:00.000Z",
            "varType": "date",
            "isInherited": false
        },
        {
            "parameterId": "end_date",
            "value": "2023-05-12T00:00:00.000Z",
            "varType": "date",
            "isInherited": false
        },
        {
            "parameterId": "simulation_granularity",
            "value": "day",
            "varType": "enum",
            "isInherited": false
        },
        {
            "parameterId": "mass_lever_excel_file", // skipped
            "value": "d-zm3lj027vq7k",
            "varType": "%DATASETID%",
            "isInherited": false
        },
        {
            "parameterId": "stock_policy",
            "value": "OrderPointFixedQuantity",
            "varType": "enum",
            "isInherited": false
        },
        {
            "parameterId": "sourcing_policy",
            "value": "HighestPriority",
            "varType": "enum",
            "isInherited": false
        },
        {
            "parameterId": "stock_dispatch_policy",
            "value": "HighestPriority",
            "varType": "enum",
            "isInherited": false
        },
        {
            "parameterId": "production_policy",
            "value": "HighestPriority",
            "varType": "enum",
            "isInherited": false
        },
        {
            "parameterId": "manage_backlog_quantities",
            "value": "false",
            "varType": "bool",
            "isInherited": false
        },
        {
            "parameterId": "empty_obsolete_stocks",
            "value": "false",
            "varType": "bool",
            "isInherited": false
        },
        {
            "parameterId": "batch_size",
            "value": "0",
            "varType": "number",
            "isInherited": false
        },
        {
            "parameterId": "financial_cost_of_stocks",
            "value": "0",
            "varType": "number",
            "isInherited": false
        },
        {
            "parameterId": "intermediary_stock_dispatch",
            "value": "DispatchAll",
            "varType": "enum",
            "isInherited": false
        }
    ]
}
```

</br>
</br>

### Set up your ```cosmotest.config.yml``` with your benchmark zip file
---

```yml
azure:
    tenant_id: yout_tenant_id
    client_id: yout_client_id
    client_secret: yout_client_secret
    cosmo_api_scope: http://dev.api.cosmotech.com/.default
    cosmo_api_host: https://dev.api.cosmotech.com

cosmo_test:
    organization:
        id: O-gZYpnd27G7                                  # your organization (required)
        name: Cosmo Tech                                  # information only (required)
    workspace:
        id: W-QPpQ47r2L9                                  # your workspace (required)
        name: Supply Chain Dev                            # information only (required)
    solution:
        id: SOL-0xAAgEvr3J                                # your solution (required)
        version: 1.0.0                                    # your solution version (required)
        name: Supply Chain Solution                       # information only (required)
    connector:
        id: c-q2859zy34wmm                                # connector AKS or ADT (required)
        name: AKS                                         # information only (required)
        url: ""                                           # URL ADT
        
    name_file_storage: scenario_demo_test.zip             # filename on your 'permformance-datasets' container
    scenarios:
        
        "1":                                              # select a name (string required)
            name: "large basicpool"                       # select a size (number or string required)
            size: 100000k                                 # select a name (string required)
            compute_size: "basicpool"                     #'basicpool' or 'highcpu'
            dataset:
                name: "performance large size basicpool"  # select a name
                path_input: "scenario_a"                  # folder name in scenario_demo_test.zip

        "2":                                            
            name: "medium basicpool"
            size: 10000k
            compute_size: "basicpool"
            dataset:
                name: "performance medium size basicpool"
                path_input: "scenario_b"                  # see notes
```

</br>
</br>

### Finally, run ```benchmark.py```
---

```bash
# python3 (linux)
python3 benchmark.py

# python (windows)
python benchmark.py
```