with results as (

  select * from {{ ref('stg_f1_results') }}

),

weather as (
    select * from {{ ref('stg_weather') }}
),

races as (

  select * from {{ ref('stg_f1_races') }}

),

circuits as (

  select * from {{ ref('stg_f1_circuits') }}

),

drivers as (

  select * from {{ ref('stg_f1_drivers') }}

),

constructors as (

  select * from {{ ref('stg_f1_constructors') }}

),

status as (

  select * from {{ ref('stg_f1_status') }}

),

int_results as (
    select
      result_id,
      results.race_id,
      race_name,
      race_year,
      race_round,
      races.circuit_id,
      circuit_name,
      race_date,
      race_time,
      results.driver_id,
      results.driver_number,
      forename ||' '|| surname as driver,
      cast(datediff('year', date_of_birth, race_date) as int) as drivers_age_years,
      driver_nationality,
      results.constructor_id,
      constructor_name,
      constructor_nationality,
      weather.prcp,
      case when weather.prcp is null then 0 else 1 end as rained,
      weather.tmin,
      weather.tmax,
      weather.tavg,
      grid,
      position,
      position_text,
      position_order,
      points,
      laps,
      results_time_formatted,
      results_milliseconds,
      fastest_lap,
      results_rank,
      fastest_lap_time_formatted,
      fastest_lap_speed,
      results.status_id,
      status,
      case when position is null then 1 else 0 end as dnf_flag
    from results

    left join races
      on results.race_id = races.race_id
    left join drivers
      on results.driver_id = drivers.driver_id
    left join constructors
      on results.constructor_id = constructors.constructor_id
    left join status
      on results.status_id = status.status_id
    left join weather
      on race_date = weather.date
    left join circuits
      on races.circuit_id = circuits.circuit_id
    where race_name = 'Italian Grand Prix'
 )

 select * from int_results
