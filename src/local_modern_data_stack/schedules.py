"""
This module defines schedules for automatically running Dagster jobs, such as
materializing dbt models at specified times.
"""

from dagster import AssetSelection, ScheduleDefinition

daily_update_schedule = ScheduleDefinition(
    name="daily_update_covid19_data_rki",
    target=AssetSelection.assets(["bronze", "covid19_data_rki"]),
    cron_schedule="0 0 * * *",
)

schedules = [daily_update_schedule]
