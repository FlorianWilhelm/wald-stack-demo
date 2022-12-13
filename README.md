Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


## Installation
brew install python@3.8, Python 3.8 needed
Doku Datensatz: https://www.tpc.org/tpc_documents_current_versions/pdf/tpcx-ai_v1.0.2.pdf

Everything is in Anaconda in the backend.
https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-packages.html#using-third-party-packages-from-anaconda

### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices

    https://miro.com/app/board/uXjVPLEqbzw=/?moveToWidget=3458764537073105352&cot=14

    https://pttljessy.medium.com/a-beginners-guide-to-dbt-data-build-tool-part-2-setup-guide-and-tips-6154c9bff07e

  dbt+snowflake+python https://www.snowflake.com/blog/modern-analytics-stack-snowpark-dbt-python/
- 
https://github.com/dbt-labs/new-python-wrench-demo/blob/main/fuzzer.ipynb


https://docs.snowflake.com/en/sql-reference/stored-procedures-python.html

```
use role accountadmin;

grant role orgadmin to user fwilhelm;
```


Referal Trail: https://trial.snowflake.com/?owner=SPN-PID-545753


Log into Snowsight, the Snowflake web interface.

Then execute
```
use role accountadmin;

grant role orgadmin to user YOUR_USERNAME;
```

Click the dropdown menu next to your login name, then click Switch Role » ORGADMIN to change to the organization administrator role.

Click Admin » Billing » Terms & Billing.

Scroll to the Anaconda section and click the Enable button. The Anaconda Packages (Preview Feature) dialog opens.

Click the link to review the Snowflake Third Party Terms.

If you agree to the terms, click the Acknowledge & Continue button.