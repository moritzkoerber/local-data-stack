SELECT *
FROM {{ ref('read') }}
WHERE run_date = current_date()
