DROP TABLE IF EXISTS bike_stations;
CREATE TABLE bike_stations (
    station_id SERIAL,
    capacity INT,
    lat FLOAT,
    lon FLOAT
);