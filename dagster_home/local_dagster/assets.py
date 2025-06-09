"""This file defines the data assets for your Dagster project, specifying how they are computed and managed.
Software defined assets are the main building blocks in Dagster. An asset is composed of three components:

Asset key or unique identifier.
An op which is a function that is invoked to produce the asset.
Upstream dependencies that the asset depends on."""

import os
from pathlib import Path

import plotly.express as px
import polars as pl
import requests
from dagster import (
    AssetCheckResult,
    AssetExecutionContext,
    MetadataValue,
    asset,
    asset_check,
)
from dagster_dbt import DbtCliResource, dbt_assets, get_asset_key_for_model
from dagster_duckdb import DuckDBResource

from .project import local_dagster


@asset(compute_kind="python", group_name="ingest")
def area1(context: AssetExecutionContext, duckdb: DuckDBResource) -> None:
    with duckdb.get_connection() as conn:
        table_name = "area1"
        schema = "local"
        conn.execute(f"create schema if not exists {schema}")

        conn.execute(
            f"create or replace table {schema}.{table_name} as select * from read_parquet('../data/area1_small.parquet')"
        )

        # Get row count for metadata
        result = conn.execute(f"select count(*) from {schema}.{table_name}").fetchone()
        # Log some metadata about the table we just wrote
        context.add_output_metadata({"num_rows": result[0]})


@asset(compute_kind="python", group_name="ingest")
def covid19_data_rki(context: AssetExecutionContext, duckdb: DuckDBResource) -> None:
    with duckdb.get_connection() as conn:
        response = requests.get("https://api.corona-zahlen.org/germany", timeout=180)
        data = pl.json_normalize(response.json())  # noqa

        table_name = "covid19_data_rki"
        schema = "local"

        conn.execute(f"create schema if not exists {schema}")
        conn.execute(
            f"create or replace table {schema}.{table_name} as select * from data"
        )

        # Get row count for metadata
        result = conn.execute(f"select count(*) from {schema}.{table_name}").fetchone()
        context.add_output_metadata({"num_rows": result[0]})


@asset_check(asset=area1)
def area1_label_check(duckdb: DuckDBResource) -> AssetCheckResult:
    with duckdb.get_connection() as conn:
        query_result = conn.execute(
            """
            select count(*) from local.area1
            where label != 0
            """
        ).fetchone()

        count = query_result[0] if query_result else 0
        return AssetCheckResult(
            passed=count == 0, metadata={"missing dimensions": count}
        )


# A Dagster asset that, when materialized, will execute dbt build for the specified dbt project, effectively running all your dbt models and tests.
@dbt_assets(manifest=local_dagster.manifest_path)
def dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


@asset(
    compute_kind="python",
    deps=[get_asset_key_for_model([dbt_assets], "write")],
)
def cases_histogram(context: AssetExecutionContext, duckdb: DuckDBResource) -> None:
    with duckdb.get_connection() as conn:
        cases = conn.sql("select * from write").pl()

        fig = px.histogram(cases, x="cases")
        fig.update_layout(bargap=0.2)
        fig.update_xaxes(categoryorder="total ascending")
        save_chart_path = Path(duckdb.database).parent.joinpath("cases_chart.html")
        fig.write_html(save_chart_path, auto_open=True)

        # Tell Dagster about the location of the HTML file,
        # so it's easy to access from the Dagster UI
        context.add_output_metadata(
            {"plot_url": MetadataValue.url(f"file://{os.fspath(save_chart_path)}")}
        )
