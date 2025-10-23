SELECT
    meta_lastupdate,
    cases
FROM {{ ref('silver_covid') }}
WHERE run_date = current_date()
