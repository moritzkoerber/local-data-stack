from dagster import AssetExecutionContext, asset
from dagster_dbt import DbtCliResource, dbt_assets
import duckdb
import os

from .project import duckdb_project


@asset(compute_kind="python")
def area1(context: AssetExecutionContext) -> None:
    connection = duckdb.connect(":memory:")
    connection.execute("create schema if not exists local")

    # Read from the parquet file and create a table
    parquet_path = "../data/area1_small.parquet"
    connection.execute(f"create or replace table local.test as select * from read_parquet('{parquet_path}')")

    # Get row count for metadata
    result = connection.execute("select count(*) from local.test").fetchone()
    # Log some metadata about the table we just wrote
    context.add_output_metadata({"num_rows": result[0]})


@dbt_assets(manifest=duckdb_project.manifest_path)
def duckdb_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
