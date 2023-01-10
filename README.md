# Benchmark performance test

Benchmark performance is a toolset to support solution to benchmark their performances.
Solution team will create their own benchmark scenarios and execute them to obtain a complete detailed overview of the platform performances.

</br>

### Prerequisites

- python >=3.9

- Storage Account (with all permissions)
  - find and note ```Account Name``` and ```Account Key``` values. You use this values later

- Registration app

  1. Sign in to the Azure portal.
  - Choose the Azure AD tenant where you want to create your applications
  - Register the app
    1. Navigate to the Azure portal and select the Azure AD service.
    2. Select the App Registrations blade on the left, then select New registration.
    3. In the Register an application page that appears, enter your application's registration information:
        * In the Name section, enter a meaningful application name that will be displayed to users of the app
        * Under Supported account types, select Accounts in this organizational directory only (cosmotech.com only - Single tenant)
        * Select Register to create the application
        * In the app's registration screen, find and note the Application (client) ID. You use this value in your app's configuration file(s) later in your code.
        * Create a client secret and note it. You use this value in your app's configuration file(s) later in your code.
        * Finally, add a permission ```Organization.Admin``` and grant admin consent for cosmotech.com
- File zip that contains scenarios to run.

```bash
# scenarios_demo.zip (example)
...
├── dataset #(required but it can be empty)
│   ├── X # match in configuration file
│   │   ├── file1.csv 
│   │   ├── file2.csv
│   │   └── file3.csv
│   ├── M # match in configuration file
│   │   ├── file1.csv
│   │   ├── file2.csv
│   │   └── file3.csv
│   └── S # match in configuration file
│       ├── file1.csv
│       ├── file2.csv
│       └── file3.csv
│
├── scenario #(required)
│   ├─ scenario1 # match in configuration file
│   │  ├── mass_lever_excel_file #(required)
│   │  │   └── lever_example.xlsx
│   │  └── scenario1.json
│   │
│   ├── scenario2 # match in configuration file
│   │  ├── mass_lever_excel_file #(required)
│   │  │   └── lever_example.xlsx
│   │  └── scenario2.json # (example)
...
```

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
python3 init.py --account_name <<ACCOUNT_NAME>> --account_key <<ACCOUNT_KEY>>

# python (windows)
python init.py --account_name <<ACCOUNT_NAME>> --account_key <<ACCOUNT_KEY>>
```

### Set up your ```cosmotest.config.yml``` with your benchmark zip file
---

```yml
azure:
  tenant_id: << tenant id >>
  client_id: << client id >>
  client_secret: << secret id >>
  cosmo_api_scope: http://dev.api.cosmotech.com/.default
  cosmo_api_host: https://dev.api.cosmotech.com

cosmo:
  organization_id: O-gZYpnd27G7
  workspace_id: w-pr920k6lre0ym
  connector: AKS
  dataset: 
    # can be empty if you don't want to create a new dataset
    - name:
      path_input:

  scenarios:

    - name: scenario1
      size: 100000k
      compute_size: basic
      # dataset name
      dataset: ADT Supplychain QA

    - name: scenario2
      size: 1000k
      compute_size: basic
      dataset: ADT Supplychain QA 

```

</br>
</br>

### Finally, run ```benchmark.py```
---

```bash
# python3 (linux)
python3 benchmark.py --supply  [--asset]

# python (windows)
python benchmark.py --supply [--asset]
```