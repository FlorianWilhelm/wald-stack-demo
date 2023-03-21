import io
import logging

import joblib
import pandas as pd
import snowflake.snowpark.functions as F
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


def save_file(session, model, path, dest_filename):
    input_stream = io.BytesIO()
    joblib.dump(model, input_stream)
    session._conn.upload_stream(input_stream, path, dest_filename)
    return "successfully created file: " + path


def model(dbt, session):
    dbt.config(
        packages=["numpy", "scikit-learn", "pandas", "numpy", "joblib", "cachetools"],
        materialized="table",
        tags="train",
    )
    # Create a stage in Snowflake to save our model file
    session.sql("create or replace stage MODELSTAGE").collect()

    # session._use_scoped_temp_objects = False
    version = "1.0"
    logger.info("Model training version: " + version)

    # Read in our training and testing upstream dataset
    test_train_df = dbt.ref("train_test_dataset")

    # Cast snowpark df to pandas df
    test_train_pd_df = test_train_df.to_pandas()
    target_col = "POSITION_LABEL"

    # split out covariate predictors, x, from our target column position_label, y.
    split_X = test_train_pd_df.drop([target_col], axis=1)
    split_y = test_train_pd_df[target_col]

    # Split out our training and test data into proportions (just for demonstration).
    # NOTE: Doing this kind of preprocessing in Pandas is actually a bad practice as we are now limited by
    # the node's memory. Better use SnowPark's internal functionality to do this. Find out more under:
    # https://docs.snowflake.com/developer-guide/snowpark/reference/python/api/snowflake.snowpark.DataFrame.random_split.html
    X_train, X_test, y_train, y_test = train_test_split(
        split_X, split_y, train_size=0.7, random_state=42
    )
    train = [X_train, y_train]
    test = [X_test, y_test]

    # Use all cores (processes instead of threading) of our warehouse node
    with joblib.parallel_backend("loky", n_jobs=-1):
        # Now we are only training our one model to deploy.
        # We focus on the workflows and not algorithms for this demonstration!
        model = LogisticRegression()

        # Fit the preprocessing pipeline and the model together
        model.fit(X_train, y_train)
        y_pred = model.predict_proba(X_train)[:, 1]

    balanced_accuracy = balanced_accuracy_score(
        y_train, [round(value) for value in y_pred]
    )
    logger.info(f"Balanced accuracy on training set: {balanced_accuracy:.2}")

    # Predict on the test set
    y_pred = model.predict_proba(X_test)[:, 1]
    balanced_accuracy = balanced_accuracy_score(
        y_test, [round(value) for value in y_pred]
    )
    logger.info(f"Balanced accuracy on training set: {balanced_accuracy:.2}")

    # Save the model to a stage
    save_file(
        session,
        model,
        "@MODELSTAGE/driver_position_" + version,
        "driver_position_" + version + ".joblib",
    )
    logger.info(
        "Model artifact:" + "@MODELSTAGE/driver_position_" + version + ".joblib"
    )

    # Take our pandas training and testing dataframes and put them back into Snowpark dataframes
    snowpark_train_df = session.write_pandas(
        pd.concat(train, axis=1, join="inner"),
        "train_table",
        auto_create_table=True,
        create_temp_table=True,
    )
    snowpark_test_df = session.write_pandas(
        pd.concat(test, axis=1, join="inner"),
        "test_table",
        auto_create_table=True,
        create_temp_table=True,
    )

    # Union our training and testing data together and add a column indicating train vs test rows
    return snowpark_train_df.with_column("DATASET_TYPE", F.lit("train")).union(
        snowpark_test_df.with_column("DATASET_TYPE", F.lit("test"))
    )
