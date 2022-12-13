import pandas as pd


def model(dbt, session):
    """Add new `weekday` columns like L_SHIPDATE_WEEKDAY"""
    dbt.config(
        materialized="table",
        packages=["pandas"],
        enabled=True
    )

    date_cols = ["L_SHIPDATE", "L_COMMITDATE", "L_RECEIPTDATE"]
    df_lineitem = dbt.source("tpch_sf1", "lineitem").to_pandas()

    for col in date_cols:
        df_lineitem = df_lineitem.assign(**{f"{col}_WEEKDAY": pd.to_datetime(df_lineitem[col]).dt.weekday})

    return df_lineitem
