use role accountadmin;

use warehouse geo_pulse_wh;

use database geo_pulse_db;

use schema geo_pulse_db.raw_data;


create file format if not exists gps_csv_format
type = 'csv'
skip_header = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
NULL_IF = ('', 'NULL');

create stage if not exists gps_stage
file_format = gps_csv_format;


SHOW STAGES IN SCHEMA GEO_PULSE_DB.RAW_DATA;

list @geo_pulse_db.raw_data.gps_stage;

SELECT
    $1, $2, $3, $4, $5, $6, $7, $8
FROM @GEO_PULSE_DB.RAW_DATA.GPS_STAGE/cleaned_data.csv
    (FILE_FORMAT => 'GEO_PULSE_DB.RAW_DATA.GPS_CSV_FORMAT')
LIMIT 5;


--store_data internal stage
create stage if not exists store_stage
file_format = gps_csv_format;

show stages;

list @geo_pulse_db.raw_data.store_stage;

select 
$1, $2, $3, $4 
from @geo_pulse_db.raw_data.store_stage/cleaned_store_data.csv
(FILE_FORMAT => 'GEO_PULSE_DB.RAW_DATA.GPS_CSV_FORMAT')
LIMIT 5;