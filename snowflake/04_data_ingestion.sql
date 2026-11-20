use role accountadmin;

use warehouse geo_pulse_wh;

use database geo_pulse_db;

use schema geo_pulse_db.raw_data;

copy into geo_pulse_db.raw_data.gps_pings(
ping_id,
device_id,
latitude,
longitude,
timestamp,
speed,
movement,
city
)FROM (
    SELECT
        $1,
        $2,
        $3,
        $4,
        $5,
        $6,
        $7,
        $8
    FROM @GEO_PULSE_DB.RAW_DATA.GPS_STAGE/cleaned_data.csv
)
FILE_FORMAT = (
    FORMAT_NAME = 'GEO_PULSE_DB.RAW_DATA.GPS_CSV_FORMAT'
)
ON_ERROR = 'ABORT_STATEMENT';


select 
count(*) as total_ping,
count(distinct device_id) as unique_device,
min(timestamp) as first_ping,
max(timestamp) as last_ping
from geo_pulse_db.raw_data.gps_pings;


UPDATE GEO_PULSE_DB.RAW_DATA.GPS_PINGS
SET LOCATION = ST_MAKEPOINT(LONGITUDE, LATITUDE)
WHERE LOCATION IS NULL
  AND LATITUDE BETWEEN -90 AND 90
  AND LONGITUDE BETWEEN -180 AND 180;

SELECT
    COUNT(*) AS TOTAL_PINGS,
    COUNT(LOCATION) AS VALID_LOCATIONS,
    COUNT(*) - COUNT(LOCATION) AS MISSING_LOCATIONS
FROM GEO_PULSE_DB.RAW_DATA.GPS_PINGS;

select * from geo_pulse_db.raw_data.gps_pings limit 10;


copy into geo_pulse_db.raw_data.store_data(
store_id,
latitude,
longitude,
city
)from(
select $1, $2, $3, $4
from @geo_pulse_db.raw_data.store_stage/cleaned_store_data.csv
)
file_format = (format_name='GEO_PULSE_DB.RAW_DATA.GPS_CSV_FORMAT') 
ON_ERROR = 'ABORT_STATEMENT';

select * from raw_data.store_data
limit 5;
