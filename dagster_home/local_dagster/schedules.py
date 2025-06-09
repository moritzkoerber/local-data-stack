"""This module defines schedules for automatically running Dagster jobs, such as materializing dbt models at specified times."""

from dagster_dbt import build_schedule_from_dbt_selection

from .assets import local_dagster_assets

schedules = [
    build_schedule_from_dbt_selection(
        [local_dagster_assets],
        job_name="materialize_dbt_models",
        cron_schedule="0 11 * * *",
        dbt_select="fqn:*",
    )
]
