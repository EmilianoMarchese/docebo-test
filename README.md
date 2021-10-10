# Transactional Data Engineer Test (docebo)

## How to reproduce
First, clone the repository 

```shell
git clone https://github.com/EmilianoMarchese/docebo-test.git
```
cd into it 

```shell
cd docebo-test
```
Before spawning the containers, make sure you don't have any service listening
at port 3306, e.g. `sudo /etc/init.d/mysql stop`.

Deploy the containers (not in daemon mode in order for logs to be visible):
```shell
docker-compose up
```

open a new shell and log into MySQL db (use the password provided by email)****
```shell
docker exec -it docebo-test-db-1 mysql -uroot -p
```

select the relevant database

```sql
use docebo
```

and test the queries provided in the [2nd part.](#2nd-part---answer-some-questions-using-sql)

## 1st part - Ingest data into a relational database from JSON files
Use of a Python-based ingestion layer to 
* dowonlad the data
* clean it using the provided info in the metadata (drop columns with `id = -1`) 
* use an ORM (SQLAlchemy) to create and populate a table named `AirQuality`
* containerize application and use docker-compose to make it reproducible

## 2nd part - Answer some questions using SQL

### 1. Sum value of "Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard" per year
```sql
select ReportYear, sum(Value) as value
from AirQuality
where MeasureName='Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard'
group by ReportYear;
```
<pre>+------------+-------+
| ReportYear | value |
+------------+-------+
|       1999 | 12501 |
|       2003 |  6442 |
|       2000 |  7780 |
|       2004 |  3428 |
|       2010 |  2514 |
|       2001 |  8402 |
|       2002 | 12142 |
|       2005 |  7057 |
|       2006 |  5343 |
|       2007 |  6044 |
|       2008 |  3181 |
|       2009 |  1497 |
|       2011 |  3173 |
|       2012 |  4233 |
|       2013 |  1186 |
+------------+-------+
</pre>

### 2. Year with max value of "Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard" from year 2008 and later (inclusive)
```sql
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
```
<pre>+------------+
|       2008 |
+------------+
</pre>

### 3. Max value of each measurement per state
```sql
select MeasureName, StateName, MAX(Value) max_value
from AirQuality
group by MeasureName, StateName
order by 1;
```
output truncated to first 10 rows

<pre>+------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+-----------+
| MeasureName                                                                                                                                                | StateName            | max_value |
+------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+-----------+
| Annual average ambient concentrations of PM 2.5 in micrograms per cubic meter, based on seasonal averages and daily measurement (monitor and modeled data) | Alabama              |        21 |
| Annual average ambient concentrations of PM 2.5 in micrograms per cubic meter, based on seasonal averages and daily measurement (monitor and modeled data) | Arizona              |        12 |
| Annual average ambient concentrations of PM 2.5 in micrograms per cubic meter, based on seasonal averages and daily measurement (monitor and modeled data) | Arkansas             |        16 |
| Annual average ambient concentrations of PM 2.5 in micrograms per cubic meter, based on seasonal averages and daily measurement (monitor and modeled data) | California           |        30 |
| Annual average ambient concentrations of PM 2.5 in micrograms per cubic meter, based on seasonal averages and daily measurement (monitor and modeled data) | Colorado             |        12 |
| Annual average ambient concentrations of PM 2.5 in micrograms per cubic meter, based on seasonal averages and daily measurement (monitor and modeled data) | Connecticut          |        17 |
| Annual average ambient concentrations of PM 2.5 in micrograms per cubic meter, based on seasonal averages and daily measurement (monitor and modeled data) | Delaware             |        18 |
| Annual average ambient concentrations of PM 2.5 in micrograms per cubic meter, based on seasonal averages and daily measurement (monitor and modeled data) | District of Columbia |        18 |
| Annual average ambient concentrations of PM 2.5 in micrograms per cubic meter, based on seasonal averages and daily measurement (monitor and modeled data) | Florida              |        14 |
| Annual average ambient concentrations of PM 2.5 in micrograms per cubic meter, based on seasonal averages and daily measurement (monitor and modeled data) | Georgia              |        19 |
+------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+-----------+
</pre>

### 4. Average value of "Number of person-days with PM2.5 over the National Ambient Air Quality Standard (monitor and modeled data)" per year and state in ascending order
```sql
select ReportYear, StateName, AVG(Value) avg_value
from AirQuality
where MeasureName='Number of person-days with PM2.5 over the National Ambient Air Quality Standard (monitor and modeled data)'
group by ReportYear, StateName
order by 3;
```
output truncated to first 10 rows

<pre>+------------+--------------+-----------+
| ReportYear | StateName    | avg_value |
+------------+--------------+-----------+
|       2008 | Nebraska     |    0.0000 |
|       2008 | Colorado     |    0.0000 |
|       2009 | Oklahoma     |    0.0000 |
|       2008 | Rhode Island |    0.0000 |
|       2009 | Rhode Island |    0.0000 |
|       2011 | Nebraska     |    0.0000 |
|       2011 | Delaware     |    0.0000 |
|       2010 | Mississippi  |    0.0000 |
|       2011 | Mississippi  |    0.0000 |
|       2008 | Oklahoma     |    0.0000 |
+------------+--------------+-----------+
</pre>

### 5. State with the max accumulated value of "Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard" overall years
```sql
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
```
<pre>+------------+
| StateName  |
+------------+
| California |
+------------+
</pre>

### 6. Average value of "Number of person-days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard" in the state of Florida
```sql
select AVG(Value) avg_value
from AirQuality
where MeasureName =
          'Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard'
and StateName='Florida'
group by StateName;
```
<pre>+-----------+
| avg_value |
+-----------+
|    3.0700 |
+-----------+
</pre>

### 7. County with min "Number of days with maximum 8-hour average ozone concentration over the National Ambient Air Quality Standard" per state per year
```sql
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
```
output truncated to first 10 rows

<pre>+------------+-----------+------------+---------+
| CountyName | StateName | ReportYear | min_val |
+------------+-----------+------------+---------+
| Sumter     | Alabama   |       1999 |       3 |
| Sumter     | Alabama   |       2000 |       5 |
| Lawrence   | Alabama   |       2001 |       1 |
| Sumter     | Alabama   |       2001 |       1 |
| Baldwin    | Alabama   |       2002 |       0 |
| Montgomery | Alabama   |       2003 |       0 |
| Russell    | Alabama   |       2003 |       0 |
| Sumter     | Alabama   |       2003 |       0 |
| Colbert    | Alabama   |       2004 |       0 |
| Etowah     | Alabama   |       2004 |       0 |
+------------+-----------+------------+---------+
</pre>