from sklearn.ensemble import RandomForestRegressor


def model(dbt, session):
    dbt.config(
        materialized="table",
        packages=["fuzzywuzzy"],
        enabled=False
    )

    date_cols = ["L_SHIPDATE", "L_COMMITDATE", "L_RECEIPTDATE"]

    df_price = dbt.ref("stg_fruit_prices_fact").to_pandas()

    def custom_scorer(string):
        '''
        for a given string
        return the best match out of the `fruit_name` column in the df_to table
        '''

        x = process.extractOne(string, df_price["fruit_name"], score_cutoff=60)

        if x is not None:
            return x[0]
        else:
            return None

    return  (dbt.ref("fruit_user_input").to_pandas()
                # make new col, `fruit_name`, with best match against actual table
                .assign(fruit_name=lambda df: df["fruit_user_input"].apply(custom_scorer))
                )