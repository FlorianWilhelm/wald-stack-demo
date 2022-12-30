"""Some simple utilities for Snowflake and dbt"""
from dbt.config import Profile
from dbt.task.base import read_profiles
from dbt.adapters.snowflake.impl import SnowflakeAdapter
from dbt.contracts.connection import Credentials
import snowflake.connector
from snowflake.connector.connection import SnowflakeConnection


def get_dbt_credentials(profile_name: str, target_name: str) -> Credentials:
    """Read the credentials from the dbt profiles, i.e. `~/.dbt/profiles.yaml`"""
    raw_profiles = read_profiles()
    creds = Profile._credentials_from_profile(raw_profiles[profile_name]["outputs"][target_name],
                                              profile_name,
                                              target_name)
    return creds


def get_snowflake_cursor_from_dbt(profile_name: str, target_name: str) -> SnowflakeConnection:
    """Generate a cursor using the dbt credentials following DRY"""
    creds = get_dbt_credentials(profile_name, target_name)
    connector = snowflake.connector.connect(
        user=creds.user,
        password=creds.password,
        account=creds.account,
        warehouse=creds.warehouse,
        database=creds.database,
        schema=creds.schema
    )
    return connector.cursor()


def get_snowflake_dbt_adapter(profile_name: str, target_name: str) -> SnowflakeAdapter:
    """Generate a dbt adapter for direct querying
    
    Replicates to some degree what dbt does internally. Meant for debugging only as this is rather a hack!

    ToDo: Generalize this by using dbt's functionality to retrieve the right adapter from the `type` field
          in the profile instead of hard-coding SnowflakeAdapter.
    """
    creds = get_dbt_credentials(profile_name, target_name)
    profile = Profile.from_credentials(creds, 1, profile_name, target_name)
    adapter = SnowflakeAdapter(profile)
    adapter.acquire_connection()
    return adapter
