<div align="center">
<img src="https://raw.githubusercontent.com/FlorianWilhelm/wald-stack-demo/main/assets/images/wald-stack-social-banner.png" alt="WALD stack logo" width="600" role="img">
</div>

# WALD: The Modern & Sustainable Analytics Stack

The name **WALD**-stack stems from the four technologies it is composed of, i.e. a cloud-computing **W**arehouse
like [Snowflake] or [Google BigQuery], the open-source data integration engine [**A**irbyte], the open-source full-stack
BI platform [**L**ightdash], and the open-source data transformation tool [**D**BT].

This demonstration projects showcases the Wald-stack in a minimal example. It makes use of the
[Kaggle Formula 1 World Championship dataset] and the data warehouse [Snowflake]. To allow the definition of
[Python]-based models within [dbt Core] also Snowflake's [Snowpark]-feature is enabled. For analytics and BI
we use the graphical BI-tool [Lightdash], which is a suitable addition from the dbt-ecosystem.

The WALD-stack is sustainable since it consists mainly of open-source technologies, however all technologies are also
offered as managed cloud services. The data warehouse itself, i.e. [Snowflake] or [Google BigQuery], is the only non-open-source
technology in the WALD-stack. In case of Snowflake, only the clients, eg. [snowflake-connector-python] and
[snowflake-snowpark-python], are available as open-source software.

To manage the Python environment and dependencies in this demonstration, we make use of [Mambaforge], which is a faster
and open-source alternative to [Anaconda].


## Getting started

1. Setting up the data **W**arehouse [Snowflake], i.e.:
   1. [register a 30-day free trial Snowflake account] and choose the standard edition, AWS as cloud provider and any
      region you want,
   2. check the Snowflake e-mail for your *account-identifier*, which is specified by the URL you are given, e.g.
      like `https://<account_identifier>.snowflakecomputing.com`,
   3. [log into Snowflake's Snowsight UI] using your *account-identifier*,
   4. check if [Snowflake's TPC-H sample database] `SNOWFLAKE_SAMPLE_DATA` is available under <kbd>Data</kbd> » <kbd>Databases</kbd>
      or create it under <kbd>Data</kbd> » <kbd>Private Sharing</kbd> » <kbd>SAMPLE_DATA</kbd> and name it `SNOWFLAKE_SAMPLE_DATA`.<br>
   5. create a new database named `MY_DB` with owner `ACCOUNTADMIN` by clicking <kbd>Data</kbd> » <kbd>Databases</kbd> » <kbd>+ Database</kbd> (upper right corner)
      and entering `MY_DB` in the emerging New Database form,
   6. [activate Snowpark and third-party packages] by clicking on your login name followed by <kbd>Switch Role</kbd> » <kbd>ORGADMIN</kbd>.
      Only if <kbd>ORGADMIN</kbd> doesn't show in the drop-down menu, go to <kbd>Worksheets</kbd> » <kbd>+ Worksheet</kbd> and execute:
      ```SQL
      use role accountadmin;

      grant role orgadmin to user YOUR_USERNAME;
      ```
      This should add `ORGADMIN` to the list. Now click <kbd>Admin</kbd> » <kbd>Billing</kbd> » <kbd>Terms & Billing</kbd>,
      and click <kbd>Enable</kbd> next to `Anaconda Python packages`. The Anaconda Packages (Preview Feature) dialog opens,
      and you need to agree to the terms by clicking <kbd>Acknowledge & Continue</kbd>.
   7. choose a warehouse (which is a compute-cluster in Snowflake-speak) by clicking on <kbd>Worksheets</kbd> and selecting
      <kbd>Tutorial 1: Sample queries on TPC-H data</kbd>. Now click on the role button showing <kbd>ACCOUNTADMIN · No Warehouse</kbd>
      on the upper right and select the warehouse <kbd>COMPUTE_WH</kbd> or create a new one. Note the name of the warehouse
      for the dbt setup later,
   8. execute *all* statements from the tutorial worksheet to see if everything was set up correctly.

2. Setting up [**D**BT] and [Snowpark] locally, i.e.:
   1. clone this repository with `git clone https://github.com/FlorianWilhelm/wald-stack-demo.git`,
   2. change into the repository with `cd wald-stack-demo`,
   3. make sure you have [Mambaforge] installed,
   4. set up the mamba environment `wald-stack` with:
      ```
      mamba create --name wald-stack -c https://repo.anaconda.com/pkgs/snowflake \
      python=3.8 numpy pandas jupyterlab dbt-core dbt-snowflake snowflake-snowpark-python snowflake-connector-python
      ```
   5. activate the environment with `mamba activate wald-stack`,
   6. create a directory `~/.dbt/` and a file `profiles.yml` in it, with content:
      ```yaml
      default:
        outputs:
          dev:
            account: your_account-identifier
            database: MY_DB
            password: your_password
            role: accountadmin
            schema: WALD_STACK_DEMO
            threads: 1
            type: snowflake
            user: your_username
            warehouse: COMPUTE_WH
        target: dev
      ```
      and set `account`, `password` as well as `user` accordingly. Also check that the value of `warehouse` corresponds
      to the one you have in Snowflake,
   7. test that your connection works by running `dbt debug`. You should see "All checks passed!"-message.

3. Setting up [**A**irbyte] locally, i.e.:
   1. make sure you have [docker] installed,
   2. install it with:
      ```commandline
      git clone https://github.com/airbytehq/airbyte.git
      cd airbyte
      docker-compose up
      ```
   3. check if the front-end comes up at [http://localhost:8000](http://localhost:8000) and log in with
      username `airbyte` and password `password`,
   4. enter some e-mail address and click continue. The main dashboard should show up.

4. Set up [**L**ightdash] locally, i.e.:
   1. make sure you have [docker] installed,
   2. install Lightdash locally by following the [local deployment instructions], i.e.:
      ```commandline
      cd .. # to leave "wald-stack-demo" if necessary
      git clone https://github.com/lightdash/lightdash
      cd lightdash
      ./scripts/install.sh # and choose "Custom install", enter the path to your dbt project from above
      ```
   3. check if the front-end comes up at [http://localhost:8080](http://localhost:8080).

## Demonstration of the WALD-stack

### Demonstration use-case

### Ingesting the weather data with Airbyte



To get our hands on some data we can ingest into our warehouse, let's just download some [weather data from opendatasoft]
and put it into our `seeds` folder. In order to do so, just run inside the `wald-stack-demo` folder:
```commandline
curl -X 'GET' \
  'https://public.opendatasoft.com/api/v2/catalog/datasets/noaa-daily-weather-data/exports/csv?limit=-1&offset=0&refine=country_code:US&refine=date:2016&timezone=UTC' \
  -H 'accept: */*' > seeds/daily_weather_us_2016.csv
```
While you wait, go and grab yourself a cup of :coffee: or :tea:. The file should have about 551MB.
After we have downloaded the file we need to copy it into the running Airbyte [docker] container with:
```commandline
docker cp seeds/daily_weather_us_2016.csv airbyte-server:/tmp/workspace/daily_weather_us_216.csv
```
It is certainly not necessary to point out that this is purely for testing the stack and in a production setting, one
would rather choose some S3 bucket or a completely different data source like [Kafka].

Before we start using Airbyte, let's first set up a new database and schema for the data we are about to ingest.
Open a notebook in Snowsight and execute:
```sql
CREATE DATABASE WEATHER;
USE DATABASE WEATHER;
CREATE SCHEMA RAW;
```

Let's fire up the Airbyte Web-GUI under [http://localhost:8000](http://localhost:8000) where you should see this after having logged in:
<div align="center">
<img src="https://raw.githubusercontent.com/FlorianWilhelm/wald-stack-demo/main/assets/images/airbyte-welcome.png" alt="Welcome screen of Airbyte" width="500" role="img">
</div>

Now click on <kbd>Create your first connection</kbd> and select `File` as source type and fill out the form like this:
<div align="center">
<img src="https://raw.githubusercontent.com/FlorianWilhelm/wald-stack-demo/main/assets/images/airbyte-source.png" alt="Source selection of Airbyte" width="500" role="img">
</div>

Hit <kbd>Set up Source</kbd> and select <kbd>Snowflake</kbd> in the next form as destination type. No you should see a detailed form
to set up the Snowflake destination. Enter the values like this with the corresponding settings from the Snowflake setup
from above. Remember that the `host` url follows the schema `<account_identifier>.snowflakecomputing.com`.
<div align="center">
<img src="https://raw.githubusercontent.com/FlorianWilhelm/wald-stack-demo/main/assets/images/airbyte-destination.png" alt="Destination selection of Airbyte" width="500" role="img">
</div>

Then hit <kbd>Set up destination</kbd> and see a new form popping up. We just stick with the sane defaults provided to us.
<div align="center">
<img src="https://raw.githubusercontent.com/FlorianWilhelm/wald-stack-demo/main/assets/images/airbyte-setup-details.png" alt="Setup details of Airbyte connection" width="500" role="img">
</div>

After hitting <kbd>Set up connection</kbd>, you should see that Airbyte starts syncing our weather data to Snowflake.
<div align="center">
<img src="https://raw.githubusercontent.com/FlorianWilhelm/wald-stack-demo/main/assets/images/airbyte-sync.png" alt="Airbyte syncs the weather data" width="500" role="img">
</div>

After about 15 minutes the sync should be successfully completed.
<div align="center">
<img src="https://raw.githubusercontent.com/FlorianWilhelm/wald-stack-demo/main/assets/images/airbyte-sync-succeeded.png" alt="Airbyte sync succeeded" width="500" role="img">
</div>

Airbyte has a lot more to offer since it has hundreds of sources and destinations for syncing. For our demonstration, however, that is all we need.
It should also be noted that uploading a simple csv file into Snowflake could also have been done using [dbt's seed] command.

### **L**ightdash

### **D**BT



## What else is to see here?

In the `notebooks` directory, you'll find two notebooks that demonstrate how [dbt] as well as the
[snowflake-connector-python] can also be directly used to execute queries for instance for debugging. In both cases
the subsystems of [dbt], and thus also the retrieval of the credentials, are used so that no credentials need to be
passed.

## Typical commands

### dbt

* **run all models**: `dbt run`
* **run all tests**: `dbt test`
* **executes snapshots**: `dbt snapshot`
* **load seed csv-files**: `dbt seed`
* **run + test + snapshot + seed in DAG order**: `dbt build`
* **download dependencies**: `dbt dep`
* **generate docs and lineage**: `dbt docs`

### Lightdash

* **restart**: `docker-compose -f docker-compose.yml start`
* **stop**: `docker-compose -f docker-compose.yml stop -v`
* **bring down and clean volumes**: `docker-compose -f docker-compose.yml down -v`


## Formula 1 World Championship Data

The following figure shows database entities, relationships, and characteristics
of the [Kaggle Formula 1 World Championship dataset], which we are using for this demonstration.

<div align="center">
<img src="https://raw.githubusercontent.com/FlorianWilhelm/wald-stack-demo/main/assets/images/db-schema.png" alt="Formula 1 database schemas" width="800" role="img">
</div>


## Credits

The dbt, Snowpark part of this demonstration is heavily based on the [python-snowpark-formula1 repository] as well as
the awesome "Advanced Analytics" online workshop by [Hope Watson] from [dbt labs] held on January 25th, 2023.


## References & Resources

Following resources were used for this demonstration project besides the ones already mentioned:

* [A Beginner’s Guide to DBT (data build tool)] by Jessica Le
* [Snowpark for Python Blog Post] by Caleb Baechtold
* [Overview Quickstart ML with Snowpark for Python] by Snowflake
* [Advanced Quickstart ML with Snowpark for Python] by Snowflake
* [Quickstart Data Engineering with Snowpark for Python and dbt] by Snowflake
* [Upgrade to the Modern Analytics Stack: Doing More with Snowpark, dbt, and Python] by Ripu Jain and Anders Swanson
* [dbt cheetsheet] by Bruno S. de Lima

## ToDos

- [ ] Find out why creating an environment file with `mamba env export --no-builds > environment.yml` and recreating
  the environment with `mamba env create -f environment.yml` fails with a lot of packages that cannot be resolved.
- [ ] Mention also Dagster as a complementary tool

[**A**irbyte]:https://airbyte.com/
[Google BigQuery]: https://cloud.google.com/bigquery
[Snowflake]: https://www.snowflake.com/
[Snowpark]: https://www.snowflake.com/snowpark/
[**L**ightdash]: https://www.lightdash.com/
[dbt]: https://www.getdbt.com/
[**D**BT]: https://www.getdbt.com/
[dbt Core]: https://github.com/dbt-labs/dbt-core
[Tableau]: https://www.tableau.com/
[Lightdash]: https://github.com/lightdash/lightdash
[snowflake-connector-python]: https://github.com/snowflakedb/snowflake-connector-python
[snowflake-snowpark-python]: https://github.com/snowflakedb/snowpark-python
[Mambaforge]: https://github.com/conda-forge/miniforge#mambaforge
[register a 30-day free trial Snowflake account]: https://trial.snowflake.com/?owner=SPN-PID-545753
[Snowflake's TPC-H sample database]: https://docs.snowflake.com/en/user-guide/sample-data-tpch.html
[log into Snowflake's Snowsight UI]: https://app.snowflake.com/
[activate Snowpark and third-party packages]: https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-packages.html
[A Beginner’s Guide to DBT (data build tool)]: https://pttljessy.medium.com/a-beginners-guide-to-dbt-data-build-tool-part-4-dbt-automation-test-and-templating-3656114a4d8d
[Upgrade to the Modern Analytics Stack: Doing More with Snowpark, dbt, and Python]: https://www.snowflake.com/blog/modern-analytics-stack-snowpark-dbt-python/
[docker]: https://www.docker.com/
[local deployment instructions]: https://docs.lightdash.com/get-started/setup-lightdash/install-lightdash/#deploy-locally-with-our-installation-script
[dbt cheetsheet]: https://github.com/bruno-szdl/cheatsheets/blob/main/dbt_cheat_sheet.pdf
[Anaconda]: https://www.anaconda.com/products/distribution
[Python]: https://www.python.org/
[weather data from opendatasoft]: https://public.opendatasoft.com/explore/dataset/noaa-daily-weather-data/
[Kafka]: https://kafka.apache.org/
[dbt's seed]: https://docs.getdbt.com/docs/build/seeds
[Snowpark for Python Blog Post]: https://medium.com/snowflake/operationalizing-snowpark-python-part-one-892fcb3abba1
[Overview Quickstart ML with Snowpark for Python]: https://quickstarts.snowflake.com/guide/getting_started_snowpark_machine_learning/
[Advanced Quickstart ML with Snowpark for Python]: https://quickstarts.snowflake.com/guide/machine_learning_with_snowpark_python
[Quickstart Data Engineering with Snowpark for Python and dbt]: https://quickstarts.snowflake.com/guide/data_engineering_with_snowpark_python_and_dbt
[Kaggle Formula 1 World Championship dataset]: https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020
[python-snowpark-formula1 repository]: https://github.com/dbt-labs/python-snowpark-formula1/
[Hope Watson]: https://www.linkedin.com/in/hopewatson/
[dbt labs]: https://www.getdbt.com/
