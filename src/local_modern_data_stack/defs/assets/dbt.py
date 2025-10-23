import json

from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

from ..resources import dbt_project
from .partitions import daily_partition

INCREMENTAL_SELECTOR = "config.materialized:incremental"


# A Dagster asset that, when materialized, will execute dbt build for the specified dbt
# project, effectively running all your dbt models and tests.
@dbt_assets(manifest=dbt_project.manifest_path, exclude=INCREMENTAL_SELECTOR)
def dbt_full_models(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream().fetch_row_counts()


@dbt_assets(
    manifest=dbt_project.manifest_path,
    select=INCREMENTAL_SELECTOR,
    partitions_def=daily_partition,
)
def incremental_dbt_models(context: AssetExecutionContext, dbt: DbtCliResource):
    time_window = context.partition_time_window
    dbt_vars = {
        "start_date": time_window.start.strftime("%Y-%m-%d"),
        "end_date": time_window.end.strftime("%Y-%m-%d"),
    }

    yield from dbt.cli(
        ["build", "--vars", json.dumps(dbt_vars)], context=context
    ).stream()
