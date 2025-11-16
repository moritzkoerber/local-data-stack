from dagster import (
    DefaultScheduleStatus,
    build_schedule_from_partitioned_job,
)

from local_modern_data_stack.defs.jobs import partitioned_asset_job

partitioned_asset_job_schedule = build_schedule_from_partitioned_job(
    job=partitioned_asset_job,
    default_status=DefaultScheduleStatus.RUNNING,
    name="daily_update_xetra",
)

schedules = [partitioned_asset_job_schedule]
