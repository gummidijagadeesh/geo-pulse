use role accountadmin;

use warehouse geo_pulse_wh;

use database geo_pulse_db;

use schema geo_pulse_db.raw_data;

create table if not exists gps_pings(
ping_id smallint,
device_id string,
latitude float,
longitude float,
timestamp timestamp_ntz,
speed float,
movement string,
city string,
location geography
);

desc table geo_pulse_db.raw_data.gps_pings;

show tables in geo_pulse_db.raw_data;
