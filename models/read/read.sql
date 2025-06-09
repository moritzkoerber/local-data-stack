SELECT
    *,
    current_date() AS run_date
FROM {{ source("covid19", "covid19_data_rki") }}
