"""Some simple utilities for Snowflake and dbt"""
import dbt
from dbt.config import Profile
from dbt.task.base import read_profiles
from dbt.adapters.snowflake.impl import SnowflakeAdapter
import snowflake.connector


def get_cursor(profile_name, target_name):
    """Generate a cursor using the dbt credentials following DRY"""
    raw_profiles = read_profiles()
    creds = Profile._credentials_from_profile(raw_profiles[profile_name]["outputs"][target_name], profile_name, target_name)
    connector = snowflake.connector.connect(
        user=creds.user,
        password=creds.password,
        account=creds.account,
        warehouse=creds.warehouse,
        database=creds.database,
        schema=creds.schema
    )
    return connector.cursor()


def get_adapter(profile_name, target_name):
    """Generate a dbt adapter for direct querying
    
    Replicates to some degree what dbt does internally. Meant for debugging only as this is rather a hack!
    """
    raw_profiles = read_profiles()
    creds = Profile._credentials_from_profile(raw_profiles[profile_name]["outputs"][target_name], profile_name, target_name)
    profile = Profile.from_credentials(creds, 1, profile_name, target_name)
    adapter = SnowflakeAdapter(profile)
    adapter.acquire_connection()
    return adapter
