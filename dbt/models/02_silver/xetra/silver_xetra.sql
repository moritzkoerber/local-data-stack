{{
    config(
        materialized="incremental",
        incremental_strategy="delete+insert",
        unique_key="trading_day",
        on_schema_change="fail",
    )
}}

select
    cast(trading_day as timestamp) as trading_day,
    cast("1. open" as float) as opening_price,
    cast("2. high" as float) as highest_price,
    cast("3. low" as float) as lowest_price,
    cast("4. close" as float) as closing_price,
    cast("5. volume" as float) as trade_volume
from {{ source("stocks", "xetra") }}
{% if is_incremental() %}
    where
        trading_day >= '{{ var("start_date") }}'
        and trading_day < '{{ var("end_date") }}'
{% endif %}
