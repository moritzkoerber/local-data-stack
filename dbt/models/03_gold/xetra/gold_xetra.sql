{{
    config(
        materialized="incremental",
        incremental_strategy="delete+insert",
        unique_key="trading_date",
        on_schema_change="fail",
    )
}}

select trading_day as trading_date, closing_price
from {{ ref("silver_xetra") }}
{% if is_incremental() %}
    where
        trading_day >= '{{ var("start_date") }}'
        and trading_day < '{{ var("end_date") }}'
{% endif %}
