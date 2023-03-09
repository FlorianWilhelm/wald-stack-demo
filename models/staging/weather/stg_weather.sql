with

source as (
    select * from {{ source('weather', 'cameri') }}
),


enriched as (
    select
        *,
        (tmin + tmax) / (CASE WHEN tmin IS NULL THEN 0 ELSE 1 END +
                         CASE WHEN tmax IS NULL THEN 0 ELSE 1 END) as tavg
    from source
)
select * from enriched
