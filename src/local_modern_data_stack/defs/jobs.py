from dagster import define_asset_job

from .assets.bronze import covid19_data_rki
from .assets.dbt import dbt_full_models, incremental_dbt_models
from .assets.presentation import cases_barchart

full_load = define_asset_job(
    name="full_pipeline_job",
    selection=[covid19_data_rki, dbt_full_models, cases_barchart],
)

partitioned_asset_job = define_asset_job(
    "partitioned_job",
    selection=[covid19_data_rki, incremental_dbt_models, cases_barchart],
)
