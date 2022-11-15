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
git clone git@github.com::Cosmo-Tech/benchmark_performance.git
cd benchmark_performance
pip install -r requirements.txt
```

After installation, you have to initialize your test environement.

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
After creation, add ```🔑 Access keys``` of your storage account

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
            "value": "%replace by config file%",
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

### Configure your ```cosmotest.config.yml``` with your benchmark zip file
---

```yml
azure:
    tenant_id: <<your_tenant_id>>
    client_id: <<your_client_id>>
    client_secret: <<your_client_secret>>
    cosmo_api_scope: http://dev.api.cosmotech.com/.default
    cosmo_api_host: https://dev.api.cosmotech.com

cosmo_test:
    organization:
        id: O-gZYpnd27G7
        name: Cosmo Tech # information only
    workspace:
        id: W-QPpQ47r2L9
        name: Supply Chain Dev # information only
    solution:
        id: SOL-0xAAgEvr3J
        name: Supply Chain Solution # information only
    connector:
        id: c-q2859zy34wmm
        name: Azure storage connector # information only

    name_file_storage: benchmark_performance.zip # benchmark zip file (example)
    scenarios:
        
        "1":
            name: "large dataset basicpool"
            size: 100000
            compute_size: "basicpool"
            dataset:
                name: "performance large size basicpool"
                path_input: "scenario_a" # folder name on benchmark zip

        "2":                                            
            name: "large dataset highcpu"
            size: 10000
            compute_size: "highcpu"
            dataset:
                name: "performance large size highcpu"
                path_input: "scenario_a" # folder name on benchmark zip
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