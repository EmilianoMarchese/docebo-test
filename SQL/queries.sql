-- 2.1 Sum value of "Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard" per year
select ReportYear, sum(Value) as value
from AirQuality
where MeasureName='Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard'
group by ReportYear
order by 1; -- bonus, just for visualization purposes

-- 2.2 Year with max value of "Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard" from year 2008 and later (inclusive)
with max_per_year as (
    select ReportYear, MAX(Value) as max_value, dense_rank() over (order by MAX(Value) desc) as DR
    from AirQuality
    where MeasureName='Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard'
    and ReportYear >= 2008
      group by ReportYear
)
select ReportYear
from max_per_year
where DR=1;

-- 2.3 Max value of each measurement per state
select MeasureName, StateName, MAX(Value) max_value
from AirQuality
group by MeasureName, StateName
order by 1;

-- 2.4 Average value of "Number of person-days with PM2.5 over the National Ambient Air Quality Standard (monitor and modeled data)" per year and state in ascending order
select ReportYear, StateName, AVG(Value) avg_value
from AirQuality
where MeasureName='Number of person-days with PM2.5 over the National Ambient Air Quality Standard (monitor and modeled data)'
group by ReportYear, StateName
order by 3;

-- 2.5 State with the max accumulated value of "Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard" overall years
with dr as (
    select StateName,
           SUM(Value)                                   sum_value,
           DENSE_RANK() over (order by SUM(Value) desc) DR
    from AirQuality
    where MeasureName =
          'Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard'
    group by StateName
)
select StateName
from dr
where DR = 1;

-- 2.6 Average value of "Number of person-days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard" in the state of Florida
select AVG(Value) avg_value
from AirQuality
where MeasureName =
          'Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard'
and StateName='Florida'
group by StateName;

-- 2.7 County with min "Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard" per state per year
with min_count_per_state as (
    select CountyName, StateName, ReportYear, MIN(Value) min_val, DENSE_RANK() over (partition by StateName, ReportYear order by MIN(Value)) DR
    from AirQuality
    where MeasureName =
              'Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard'
    group by StateName, CountyName, ReportYear
)
select CountyName, StateName, ReportYear, min_val
from min_count_per_state
where DR=1;