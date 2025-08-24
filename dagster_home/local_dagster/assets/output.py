import os
from pathlib import Path

import plotly.express as px
from dagster import (
    AssetExecutionContext,
    MetadataValue,
    asset,
)
from dagster_dbt import get_asset_key_for_model
from dagster_duckdb import DuckDBResource

from .dbt import dbt_assets


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
