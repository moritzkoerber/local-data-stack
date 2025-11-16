from dagster import Definitions

from local_modern_data_stack.defs.assets.bronze import raw_xetra
from local_modern_data_stack.defs.assets.dbt import incremental_dbt_models
from local_modern_data_stack.defs.assets.presentation import xetra_closing_price_plot
from local_modern_data_stack.defs.jobs import partitioned_asset_job
from local_modern_data_stack.defs.resources import dbt_resource, duckdb_resource
from local_modern_data_stack.defs.schedules import schedules

defs = Definitions(
    assets=[
        raw_xetra,
        incremental_dbt_models,
        xetra_closing_price_plot,
    ],
    schedules=schedules,
    jobs=[partitioned_asset_job],
    resources={"dbt": dbt_resource, "duckdb": duckdb_resource},
)
