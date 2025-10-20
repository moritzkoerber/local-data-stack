"""
This module defines schedules for automatically running Dagster jobs, such as
materializing dbt models at specified times.
"""

from dagster import DefaultScheduleStatus, ScheduleDefinition

from .defs.jobs import all_assets_job

daily_update_schedule = ScheduleDefinition(
    name="daily_update_covid19_data_rki",
    job=all_assets_job,
    cron_schedule="0 0 * * *",
    default_status=DefaultScheduleStatus.RUNNING,
)

schedules = [daily_update_schedule]
