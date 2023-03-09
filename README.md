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
   4. install the `lightdash` CLI command following the [how-to-install-the-lightdash-cli] docs.
   5. authenticate the CLI and connect the `wald_stack` dbt project by running `lightdash login http://localhost:8080`.


## Demonstration of the WALD-stack

To demonstrate the power of the WALD stack we will:

1. ingest a Formula 1 dataset into [Snowflake] using Snowflake's internal capabilities,
2. use [Airbyte] to exemplify how external data sources, in our case a csv file with weather information, can be ingested into Snowflake,
3. use [dbt] to transform the raw data using SQL and Python leveraging [Snowpark] for data analysis as well as train & predict the position in a race using some simple [Scikit-Learn] model,
4. use [Lightdash] to visualise the results and demonstrate its ad-hoc analysis capabilities.

### Ingesting the Formula 1 Dataset

To have same data to play around we are going to use the [Kaggle Formula 1 World Championship dataset], which is luckily
available on some S3 bucket. To ingest the data into Snowflake, just execute the script [ingest_formula1_from_s3_to_snowflake.sql]
within a notebook of the Snowsight UI. Just select all rows and hit the run button.

The following figure shows database entities, relationships, and characteristics of the data:

<div align="center">
<img src="https://raw.githubusercontent.com/FlorianWilhelm/wald-stack-demo/main/assets/images/db-schema.png" alt="Formula 1 database schemas" width="800" role="img">
</div>

### Ingesting the weather data with Airbyte

To get our hands on some data we can ingest into our warehouse, let's take some [weather data from opendatasoft], which
is located in the `seeds` folder. For Airbyte to find it, we need to copy it into the running Airbyte [docker] container with:
```commandline
docker cp seeds/cameri_weather.csv airbyte-server:/tmp/workspace/cameri_weather.csv
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

For the `Reader Options`, just copy & paste the following string:

```json
{"sep":";", "header": 0, "names": ["ghcn_din", "date", "prcp", "snow", "tmax", "tmin", "elevation", "name", "coord", "country_code"]}
```

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

After roughly a minute, the sync should be successfully completed.
<div align="center">
<img src="https://raw.githubusercontent.com/FlorianWilhelm/wald-stack-demo/main/assets/images/airbyte-sync-succeeded.png" alt="Airbyte sync succeeded" width="500" role="img">
</div>

Airbyte has a lot more to offer since it has hundreds of sources and destinations for syncing. For our demonstration, however, that is all we need.
Note that Airbyte integrates nicely with [dbt] and you can even specify your dbt transformations in Airbyte directly. There is much more to discover here :-)
It should also be noted that uploading a simple csv file into Snowflake could also have been done using [dbt's seed] command.

### **D**BT

Since everything is already set up for you in this repository, all you need to do is run dbt with `dbt run` and you should
see an output like this:
```commandline
16:30:55  Running with dbt=1.3.1
16:30:55  Found 22 models, 17 tests, 0 snapshots, 0 analyses, 501 macros, 0 operations, 3 seed files, 9 sources, 0 exposures, 0 metrics
16:30:55
16:30:57  Concurrency: 1 threads (target='dev')
16:30:57
16:30:57  1 of 22 START sql view model WALD_STACK_DEMO.stg_f1_circuits ................... [RUN]
16:30:58  1 of 22 OK created sql view model WALD_STACK_DEMO.stg_f1_circuits .............. [SUCCESS 1 in 0.75s]
16:30:58  2 of 22 START sql view model WALD_STACK_DEMO.stg_f1_constructors ............... [RUN]
16:30:59  2 of 22 OK created sql view model WALD_STACK_DEMO.stg_f1_constructors .......... [SUCCESS 1 in 1.06s]
16:30:59  3 of 22 START sql view model WALD_STACK_DEMO.stg_f1_drivers .................... [RUN]
16:31:00  3 of 22 OK created sql view model WALD_STACK_DEMO.stg_f1_drivers ............... [SUCCESS 1 in 0.75s]
16:31:00  4 of 22 START sql view model WALD_STACK_DEMO.stg_f1_lap_times .................. [RUN]
16:31:00  4 of 22 OK created sql view model WALD_STACK_DEMO.stg_f1_lap_times ............. [SUCCESS 1 in 0.73s]
16:31:00  5 of 22 START sql view model WALD_STACK_DEMO.stg_f1_pit_stops .................. [RUN]
16:31:01  5 of 22 OK created sql view model WALD_STACK_DEMO.stg_f1_pit_stops ............. [SUCCESS 1 in 0.72s]
16:31:01  6 of 22 START sql view model WALD_STACK_DEMO.stg_f1_races ...................... [RUN]
16:31:02  6 of 22 OK created sql view model WALD_STACK_DEMO.stg_f1_races ................. [SUCCESS 1 in 0.77s]
16:31:02  7 of 22 START sql view model WALD_STACK_DEMO.stg_f1_results .................... [RUN]
16:31:03  7 of 22 OK created sql view model WALD_STACK_DEMO.stg_f1_results ............... [SUCCESS 1 in 0.70s]
16:31:03  8 of 22 START sql view model WALD_STACK_DEMO.stg_f1_status ..................... [RUN]
16:31:03  8 of 22 OK created sql view model WALD_STACK_DEMO.stg_f1_status ................ [SUCCESS 1 in 0.67s]
...
```
Using the Snowsight UI you can now explore the created tables in the database `MY_DB`. From an analyst's perspective,
the tables created from [models/marts/aggregates] are interesting as here Python is used to retrieve summary statistics
about pit stops by constructor in table `FASTEST_PIT_STOPS_BY_CONSTRUCTOR` and the 5-year rolling average of pit stop times
alongside the average for each year is shown in table `LAP_TIMES_MOVING_AVG`.

From a data scientist's perspective, it's really nice to see how easy it is to use Python ecosystem to a train model,
store it away using a Snowflake stage and loading it again for prediction. Check out the files under [models/marts/ml]
to see how easy that is with [Snowpark] and also take a look at the resulting tables `TRAIN_TEST_POSITION` and `PREDICT_POSITION`.

Besides transformations, [dbt] has much more to offer like unit tests. Run some predefined unit test examples with `dbt test`.
Another outstanding feature of dbt is how easy it is to create useful documentation for your users and yourself. To test
it just run `dbt docs generate` followed by `dbt docs serve --port 8081` (on the default port 8080 Lightdash is running)
and open [http://localhost:8081](http://localhost:8081). In this web ui you can explore your tables, columns, metrics, etc.
and even get a useful lineage graph of your data:

<div align="center">
<img src="https://raw.githubusercontent.com/FlorianWilhelm/wald-stack-demo/main/assets/images/dbt-lineage-graph.png" alt="dbt lineage graph" width="800" role="img">
</div>

Finally, don't forget to check out the [References & Resources](#references--resources) for more information on learning dbt.

### **L**ightdash

* always use `lightdash before`



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
* **lightdash CLI**: `lightdash`

## References & Resources
<a name="references--resources"></a>

Following resources were used for this demonstration project besides the ones already mentioned:

* [A Beginner’s Guide to DBT (data build tool)] by Jessica Le
* [Snowpark for Python Blog Post] by Caleb Baechtold
* [Overview Quickstart ML with Snowpark for Python] by Snowflake
* [Advanced Quickstart ML with Snowpark for Python] by Snowflake
* [Quickstart Data Engineering with Snowpark for Python and dbt] by Snowflake
* [Upgrade to the Modern Analytics Stack: Doing More with Snowpark, dbt, and Python] by Ripu Jain and Anders Swanson
* [dbt cheetsheet] by Bruno S. de Lima


## Credits

The dbt, Snowpark part of this demonstration is heavily based on the [python-snowpark-formula1 repository] as well as
the awesome "Advanced Analytics" online workshop by [Hope Watson] from [dbt labs] held on January 25th, 2023.


## ToDos

- [ ] Find out why creating an environment file with `mamba env export --no-builds > environment.yml` and recreating
  the environment with `mamba env create -f environment.yml` fails with a lot of packages that cannot be resolved.
- [ ] Mention also Dagster as a complementary tool

[**A**irbyte]:https://airbyte.com/
[Airbyte]:https://airbyte.com/
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
[ingest_formula1_from_s3_to_snowflake.sql]: ./setup_scripts/ingest_formula1_from_s3_to_snowflake.sql
[Scikit-Learn]: https://scikit-learn.org/
[models/marts/aggregates]: ./models/marts/aggregates/
[models/marts/ml]: ./models/marts/ml/
[how-to-install-the-lightdash-cli]: https://docs.lightdash.com/guides/cli/how-to-install-the-lightdash-cli
