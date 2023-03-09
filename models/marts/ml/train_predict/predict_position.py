"""Predict the position on the hold-out dataset"""
import os

import joblib
import pandas as pd
from snowflake.snowpark import types as T
from snowflake.snowpark.functions import udf

DB_STAGE = "MODELSTAGE"
version = "1.0"
# The name of the model file
model_file_path = "driver_position_" + version
model_file_packaged = "driver_position_" + version + ".joblib"

# This is a local directory, used for storing the various artifacts locally
LOCAL_TEMP_DIR = "/tmp/driver_position"
DOWNLOAD_DIR = os.path.join(LOCAL_TEMP_DIR, "download")
TARGET_MODEL_DIR_PATH = os.path.join(LOCAL_TEMP_DIR, "ml_model")
TARGET_LIB_PATH = os.path.join(LOCAL_TEMP_DIR, "lib")

# The feature columns that were used during model training
# and that will be used during prediction
FEATURE_COLS = [
    "RACE_YEAR",
    "CIRCUIT_NAME",
    "GRID",
    "CONSTRUCTOR_NAME",
    "DRIVER",
    "DRIVERS_AGE_YEARS",
    "DRIVER_CONFIDENCE",
    "CONSTRUCTOR_RELIABILITY",
    "TOTAL_PIT_STOPS_PER_RACE",
]


def load_model_from_stage(p_session):
    p_session.file.get(
        f"@{DB_STAGE}/{model_file_path}/{model_file_packaged}", DOWNLOAD_DIR
    )
    model_fl_path = os.path.join(DOWNLOAD_DIR, model_file_packaged)
    model = joblib.load(model_fl_path)
    return model


def model(dbt, session):
    dbt.config(
        packages=[
            "snowflake-snowpark-python",
            "scipy",
            "scikit-learn",
            "pandas",
            "numpy",
        ],
        materialized="table",
        tags="predict",
    )
    # load model from ModelStage
    model = load_model_from_stage(session)

    @udf
    def predict_position(
        p_df: T.PandasDataFrame[int, int, int, int, int, int, int, int, int]
    ) -> T.PandasSeries[int]:
        # Snowpark currently does not set the column name in the input dataframe
        # The default col names are like 0,1,2,... Hence we need to reset the column
        # names to the features that we initially used for training.
        p_df.columns = [*FEATURE_COLS]
        pred_array = model.predict(p_df)
        # Convert to series
        return pd.Series(pred_array)

    # reference training to make sure it ran at least once
    dbt.ref("train_test_position")

    # Retrieve the data, and perform the prediction
    snow_df = dbt.ref("hold_out_dataset_for_prediction").select(*FEATURE_COLS)

    # Perform prediction and note that we are passing the column names!
    return snow_df.withColumn("position_predicted", predict_position(*FEATURE_COLS))
