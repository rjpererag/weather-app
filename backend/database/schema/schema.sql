CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS status(
    id NUMERIC PRIMARY KEY NOT NULL,
    status VARCHAR(500) NOT NULL
);

CREATE TABLE IF NOT EXISTS coordinates(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    city_name VARCHAR(500) NOT NULL,
    longitude NUMERIC NOT NULL,
    latitude NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_layer(
    id VARCHAR(500) PRIMARY KEY NOT NULL,
    api_response JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS processed_layer(
    id VARCHAR(500) PRIMARY KEY NOT NULL,
    raw_layer_id VARCHAR(500) NOT NULL,
    coordinates_id UUID NOT NULL,
    general_statistics JSON NOT NULL,
    weather_statistics JSON NOT NULL,
    precipitation_statistics JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

    CONSTRAINT fk_raw_layer_id FOREIGN KEY (raw_layer_id) REFERENCES raw_layer(id) ON DELETE CASCADE,
    CONSTRAINT fk_coordinates_id FOREIGN KEY (coordinates_id) REFERENCES coordinates(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transactions(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    payload JSON NOT NULL,
    status_id NUMERIC NOT NULL,
    results_id VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

    CONSTRAINT fk_status_id FOREIGN KEY (status_id) REFERENCES status(id) ON DELETE CASCADE,
    CONSTRAINT fk_results_id FOREIGN KEY (results_id) REFERENCES processed_layer(id) ON DELETE CASCADE
);