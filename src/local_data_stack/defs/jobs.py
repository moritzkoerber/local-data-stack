from dagster import define_asset_job

from local_data_stack.defs.assets.bronze import raw_xetra
from local_data_stack.defs.assets.dbt import incremental_dbt_models
from local_data_stack.defs.assets.presentation import xetra_closing_price_plot

partitioned_asset_job = define_asset_job(
    "partitioned_job",
    selection=[raw_xetra, incremental_dbt_models, xetra_closing_price_plot],
)
