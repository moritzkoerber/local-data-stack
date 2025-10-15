import dagster

all_assets_job = dagster.define_asset_job(name="full_pipeline_job")
