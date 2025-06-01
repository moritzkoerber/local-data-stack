from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import area1, duckdb_dbt_assets
from .project import duckdb_project
from .schedules import schedules

defs = Definitions(
    assets=[duckdb_dbt_assets,area1],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=duckdb_project),
    },
)
