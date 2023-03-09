with lap_times as (

  select * from {{ ref('stg_f1_lap_times') }}

),

races as (

  select * from {{ ref('stg_f1_races') }}

),

drivers as (

  select * from {{ ref('stg_f1_drivers') }}

),

expanded_lap_times_by_year as (
    select
        lap_times.race_id,
        lap_times.driver_id,
        driver_ref,
        race_year,
        race_name,
        lap,
        lap_time_milliseconds,
        lap_time_milliseconds / 1000 as lap_time_seconds
    from lap_times
    left join races
        on lap_times.race_id = races.race_id
    left join drivers
        on lap_times.driver_id = drivers.driver_id
    where lap_time_milliseconds is not null
)

select * from expanded_lap_times_by_year
