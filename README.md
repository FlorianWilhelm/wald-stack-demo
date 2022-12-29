# Demonstration Project for Snowpark on Snowflake, dbt & Lightdash  

This demonstration projects make use of the [TPC-H dataset] by the [Transaction Processing Performance Council (TPC)]
to showcase the combination of [dbt] with the data warehouse [Snowflake], its Python support [Snowpark] and the 
full-stack [BI platform Ligthdash], which is an alternative to [Tableau]. Wherever possible, we use the open-source versions, 
i.e. a local installation of [dbt Core] and [Lightdash]. For [Snowflake] and [Snowpark] only the clients, i.e.   
[snowflake-connector-python] and [snowflake-snowpark-python] are available as open-source software. To manage the
Python environment and dependencies we make use of [Mambaforge], which is a faster and open-source alternative to [Anaconda].


## Getting started

1. Set up the data Warehouse [Snowflake], i.e.:
   1. [register a 30-day free trial Snowflake account] and remember your *account-identifier*,
   2. [log into Snowflake's Snowsight UI] using your *account-identifier*,
   3. get [Snowflake's TPC-H sample database] with <kbd>Data</kbd> » <kbd>Private Sharing</kbd> » <kbd>SAMPLE_DATA</kbd> and name it `SAMPLEDB`.
      <img src="https://raw.githubusercontent.com/FlorianWilhelm/dbt_snowflake_showcase/master/assets/images/share_sample_data.png" alt="Share SAMPLE_DATA" width="500" role="img"><br>
      <img src="https://raw.githubusercontent.com/FlorianWilhelm/dbt_snowflake_showcase/master/assets/images/db_of_sample_data.png" alt="Create DB SAMPLEDB" width="500" role="img">
   4. [activate Snowpark and third-party packages] with <kbd>Worksheets</kbd> » <kbd>+ Worksheet</kbd> and execute:
      ```SQL
      use role accountadmin;

      grant role orgadmin to user USERNAME;
      ```
      Even on a trial account you should then be able to switch to role ORGADMIN by clicking on your login name followed by 
      <kbd>Switch Role</kbd> » <kbd>ORGADMIN</kbd>. Then click <kbd>Admin</kbd> » <kbd>Billing</kbd> » <kbd>Terms & Billing</kbd>,
      scroll to the Anaconda section and click the Enable button. The Anaconda Packages (Preview Feature) dialog opens and
      you need to agree to the terms by clicking the Acknowledge & Continue button.

2. Set up your local machine for dbt and Snowpark, i.e.:
   1. clone this repository with `https://github.com/FlorianWilhelm/dbt_snowflake_showcase.git`,
   2. change into the repository with `cd dbt_snowflake_showcase`,
   3. make sure you have [Mambaforge] installed,
   4. set up the mamba environment `dbt_snowflake_showcase` with: 
      ```
      mamba create --name dbt_snowflake_showcase --override-channels -c https://repo.anaconda.com/pkgs/snowflake \
      python=3.8 numpy pandas jupyterlab dbt-core dbt-snowflake snowflake-snowpark-python snowflake-connector-python
      ```
   5. activate the environment with `mamba activate dbt_snowflake_showcase`,
   6. create a directory `~/.dbt/` and add a file `profiles.yml` with content:
      ```yaml
      default:
        outputs:
          dev:
            account: your_account-identifier
            database: MYDB
            password: your_password
            role: accountadmin
            schema: MySchema
            threads: 1
            type: snowflake
            user: your_user_name
            warehouse: TPCDS_BENCH_10T
        target: dev
      ```
      and set `account`, `password` as well as `user` accordingly,
   7. test that your connection works by running `dbt debug`. You should see "All checks passed!"-message.

3. Set up [Lightdash] locally, i.e.:
   1. make sure you have [docker] installed,
   2. install Lightdash locally by following the [local deployment instructions], i.e.:
      ```commandline
      cd .. # leave "dbt_snowflake_showcase" if necessary
      git clone https://github.com/lightdash/lightdash
      cd lightdash
      ./scripts/install.sh # and choose "Custom install"
      ```
   3. check if the front-end comes up at [http://localhost:8080](http://localhost:8080).


## Typical commands

### Lightdash

* **restart**: `docker-compose -f docker-compose.yml start`
* **stop**: `docker-compose -f docker-compose.yml stop -v`
* **bring down and clean volumes**: `docker-compose -f docker-compose.yml down -v`

## TPC-H Sample Data

The following figure from the [TPC-H Benchmark documentation] shows database entities, relationships, and characteristics
of the data we are using for this demonstration.

<div align="center">
<img src="https://raw.githubusercontent.com/FlorianWilhelm/dbt_snowflake_showcase/master/assets/images/tpch.png" alt="TPC-H table metadata" width="500" role="img">
</div>

## Resources

Following resources were used for this demonstration project besides the ones already mentioned:

* [A Beginner’s Guide to DBT (data build tool)] by Jessica Le
* [Sample queries from tpch-dbgen] by Dragan Sahpaski 
* [Upgrade to the Modern Analytics Stack: Doing More with Snowpark, dbt, and Python]

## ToDos

* Find out why creating an environment file with `mamba env export --no-builds > environment.yml` and recreating 
  the environment with `mamba env create -f environment.yml` fails with a lot of packages that cannot be resolved.

[TPC-H dataset]: https://www.tpc.org/tpc_documents_current_versions/pdf/tpc-h_v3.0.1.pdf
[Transaction Processing Performance Council (TPC)]: https://www.tpc.org/
[Snowflake]: https://www.snowflake.com/
[Snowpark]: https://www.snowflake.com/snowpark/
[BI platform Ligthdash]: https://www.lightdash.com/
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
[TPC-H Benchmark documentation]: https://www.tpc.org/tpc_documents_current_versions/pdf/tpc-h_v2.17.1.pdf
[A Beginner’s Guide to DBT (data build tool)]: https://pttljessy.medium.com/a-beginners-guide-to-dbt-data-build-tool-part-4-dbt-automation-test-and-templating-3656114a4d8d
[Sample queries from tpch-dbgen]: https://github.com/dragansah/tpch-dbgen/tree/master/queries
[Upgrade to the Modern Analytics Stack: Doing More with Snowpark, dbt, and Python]: https://www.snowflake.com/blog/modern-analytics-stack-snowpark-dbt-python/
[docker]: https://www.docker.com/
[local deployment instructions]: https://docs.lightdash.com/get-started/setup-lightdash/install-lightdash/#deploy-locally-with-our-installation-script
