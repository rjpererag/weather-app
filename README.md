# Weather Data API

A Flask-based REST API to retrieve and process weather and precipitation statistics by leveraging on
asynchronous task processing.

## 📋 Table of Contents

- [Overview](#overview)

- [Features](#features)

- [Architecture](#architecture)

- [Prerequisites](#prerequisites)

- [Installation](#installation)

- [Configuration](#configuration)

- [API Documentation](#api-documentation)

- [Testing](#testing)

- [Docker Deployment](#docker-deployment)

- [Development](#development)

## Overview

This API provides weather statistics using a city name or coordinates (longitude and latitude). It features an
asynchronous architecture processing data in the background so we can later access to its results. The API will handle
database transactions (SELECT, INSERT and UPDATE) to collect or create cached data with support of third-party
API (OpenMeteo) when we need to ingest new data. 


## Features

- **Asynchronous Processing**: Non-blocking API responses with Celery task queue
- **Transaction Monitoring**: Track request status through unique transaction IDs
- **Data Layering**: Raw and processed data layers for optimal performance
- **Third-party Integration**: Automatic data fetching from external weather APIs when needed
- **PostgreSQL Database**: Robust data persistence and transaction management
- **Redis Cache**: Fast message brokering and result backend
- **Docker Support**: Full containerization with Docker Compose
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Testing Suite**: Complete test coverage with unittest

## Architecture
### API
```
        ┌─────────────┐
        │   Client    │
        └──────┬──────┘
               │
               │ GET /coordinates/<string:city_name>'
               ▼
        ┌─────────────────┐
 1)     │   Flask API     │ ◄──── Returns latitude and longitude from coordinates table (data caching)
        └────────┬────────┘       if not found in DB calls third party API ("https://geocoding-api.open-meteo.com/v1/search")
                 │
                 │
                 │ POST '/weather-data/latitude/longitude/start_date/end_date>'
                 ▼
        ┌─────────────────┐
 2)     │   Flask API     │ ◄──── Creates transaction (status: 0)
        └────────┬────────┘       Returns transaction ID immediately and starts background processing
                 │
                 │ 
                 ▼
        ┌───────────────────────┐
        │  Return trasaction ID │ 
        └────────┬──────────────┘
                 │
                 │  GET '/get-status/<string:transaction_id>'
                 │ 
                 ▼
        ┌─────────────────┐
 3)     │   Flask API     │ ◄────  Monitors transaction status (processing, ready or failed).
        └────────┬────────┘             ▲
                 │                      │ 
                 │                      │  Wait until background finishes.
                 │                      │ 
                 ▼
        ┌─────────────────────┐
        │ Validate status API │ ◄────  True IF status = processing or status = "failed ELSE False.
        └────────┬────────────┘       
                 │
                 │  GET '/search-results/transaction_id'
                 │
                 ▼
        ┌─────────────────┐
 4)     │   Flask API     │ ◄──── Returs the processed data (ready or failed)
        └────────┬────────┘       
                 │
                 │ 
                 ▼
        ┌─────────────────┐
        │    RESPONSE     │
        └─────────────────┘       
```

### Background processing
This is the background processing to collect the data from the DB if present or leveraging on the third party API
provider (https://archive-api.open-meteo.com/v1/archive).
```
        ┌──────────────────┐
        │ Check raw Layer  │ ◄──── Checks the raw layer for an API response collected before and the ID referring to
        └────────┬─────────┘       the processed layer that stores the required processed data.
                 │
                 │
                 │ 
                 ▼
        ┌─────────────────┐     FALSE   ┌──────────────────┐            ┌───────────────────┐
        │Validate response│ ----------> │Call 3rd party API│----------> │Insert in raw layer│
        └────────┬────────┘             └──────────────────┘            └─────────┬─────────┘
                 │                                                                │
                 │  TRUE.                                                         │
                 │                                                                │
                 ▼                                                                │
        ┌─────────────────────────┐                                               │
        │ Return Process layer ID │ ◀----------------------------------------------
        └────────┬────────────────┘
                 │
                 │
        ┌───────────────────────┐
        │ Check Processed Layer │ ◄──── Checks the processed layer for valid statistics processed before
        └────────┬──────────────┘    
                 │
                 │
                 │ 
                 ▼
        ┌─────────────────┐     FALSE   ┌────────────────────┐            ┌─────────────────────────┐
        │Validate response│ ----------> │Process API RESPONSE│----------> │Insert in processed layer│
        └────────┬────────┘             └────────────────────┘            └───────────┬─────────────┘
                 │                       Call StatsGenerator                          │
                 │  TRUE.                                                             │
                 │                                                                    │
                 ▼                                                                    │
        ┌───────────────────────────┐                                                 │
        │ Upsate Transaction.status │ ◀------------------------------------------------
        └────────┬──────────────────┘
                 │
                 │
                 │ 
                 ▼
        ┌─────────────────┐
        │    FINISH       │ Return an array with the paylaod and the processed data.
        └─────────────────┘   
```

This architecture represents the logic to collect the weather statistics based using available endpoint
but to avoid too many API requests a dedicated endpoint is available that orchestrate the pipeline without
HTTP request

- **/city-stats/start_date/end_date**: this endpoint will return all the processed data from the specified arguments
- **/city-stats/start_date/end_date/stats**: this endpoint will return the filtered statistics using the specified arguments,
you can collect using general, weather or precipitation.

## Prerequisites

### Local Development
- Python 3.10+
- PostgreSQL 13+
- Redis 8+
- pip (Python package manager)

### Docker Deployment
- Docker 20.10+
- Docker Compose 2.0+

## Installation

1. **Clone the repository**
```bash
git clone git@github.com:rjpererag/weather-app.git
```

### Option 1: Using make file (Recommended)
Handles .env creation with default values, builds and start containers.
```bash
# Using Makefile
make start-app
```

### Option 2:

2. **Create .env file**: If want to use default values to run in local.

```bash
# Using Makefile
make create_env
```

```bash
# Using bash
chmod +x create_env.sh
./create_env.sh
```

3. **Start services**

```bash
# Using Makefile: build docker images and start containers
make start-docker-fresh
```

```bash
# Using Makefile:  start containers
make start-docker
```

```bash
# Using bash
docker-compose up -d --build
# Or
docker-compose up -d
```
4. **Stop services**

```bash
# Using Makefile: stop containers
make stop-app
```

```bash
# Using Makefile:  stop containers and removes volumes
make stop-docker-full
```

## Configuration

Create a `.env` file in the project root:
```env
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis (automatically configured in docker-compose)
REDIS_URL=redis://redis:6379/0

# Database URL (automatically configured in docker-compose)
DATABASE_URL=postgresql://your_user:your_password@db:5432/weather_db
```

## API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Request Coordinates Data
```http
GET /coordinates/<city_name>
```

**Parameters**
- `city_name` (string): City name (e.g "Madrid")

**Example Request**
```bash
curl -X GET http://localhost:5001/coordinates/madrid
```

**Response**
```json

{
  "city_name": "madrid",
  "coordinates_id": "555f8a15-7a66-4ce3-9b7e-dce203eef827",
  "latitude": 40.4165,
  "longitude": -3.70256
}
```

#### 2. Request Weather data
```http
POST /weather-data/<latitude>/<longitude>/<start_date>/<end_date>'
```

**Parameters**
- `latitude` (string): Latitude (e.g "40.4165")
- `longitude` (string): Longitude (e.g "-3.70256")
- `start_date` (string): Start date in format yyy-mm-dd (e.g "2024-01-01")
- `end_date` (string): End date in format yyy-mm-dd (e.g "2024-01-02")

**Example Request**
```bash
curl -X POST http://localhost:5001/weather-data/40.4165/-3.70256/2024-01-01/2024-01-02
```

**Response**
```json

{
  "id_to_monitor": "f0f90c25-63b9-4f9a-806f-c93b02970579"
}
```

#### 3. Request Transaction status
```http
GET /get-status/<transaction_id>
```

**Parameters**
- `transaction_id` (string): Transaction ID (e.g "f0f90c25-63b9-4f9a-806f-c93b02970579")

**Example Request**
```bash
curl -X GET http://localhost:5001/get-status/f0f90c25-63b9-4f9a-806f-c93b02970579
```

**Response**
```json
{
  "status": "processing"
}
```

#### 4. Request Search results
```http
GET /search-results/<transaction_id>
```

**Parameters**
- `transaction_id` (string): Transaction ID (e.g "f0f90c25-63b9-4f9a-806f-c93b02970579")

**Example Request**
```bash
curl -X GET http://localhost:5001/search-results/f0f90c25-63b9-4f9a-806f-c93b02970579
```

**Response**
```json
{
  "created_at": "2025-10-30 12:22:17.114397",
  "general_statistics": {
    "days_with_precipitation": 1,
    "end": "2024-01-02",
    "precipitation_max": {
      "date": "2024-01-02T18:00",
      "value": 0.1
    },
    "precipitation_total": 1,
    "start_date": "2024-01-01",
    "temperature_average": 5.31875,
    "temperature_max": {
      "date": "2024-01-01T15:00",
      "value": 9.3
    },
    "temperature_min": {
      "date": "2024-01-02T07:00",
      "value": 1.7
    }
  }, 
  "id": "pl_-3.70256_-3.70256_2024-01-01_2024-01-02",
  "precipitation_statistics": {
    "average": 0.0020833333333333333, 
    "days_with_precipitation": 1, 
    "max": {
      "date": "2024-01-02T18:00", 
      "value": 0.1
    }, "total": 1, 
    "total_by_day": {
      "2024-01-01": 0.0, 
      "2024-01-02": 0.1
    }
  }, 
  "weather_statistics": {
    "average": 5.31875, 
    "average_by_day": {
      "2024-01-01": 4.8125, 
      "2024-01-02": 5.825
    }, 
    "hours_above_threshold": 0, 
    "hours_below_threshold": 2, 
    "max": {
      "date": "2024-01-01T15:00", 
      "value": 9.3
    }, 
    "min": {
      "date": "2024-01-02T07:00", 
      "value": 1.7
    }
  }
}
```
#### 5. Request City stats
```http
GET /city-stats/<city_name>/<start_date>/<end_date>
```

**Parameters**
- `city_name` (string): City name (e.g "lisboa")
- `start_date` (string): Start date in format yyy-mm-dd (e.g "2024-01-01")
- `end_date` (string): End date in format yyy-mm-dd (e.g "2024-01-02")

**Example Request**
```bash
curl -X GET http://localhost:5001/city-stats/lisboa/2024-01-01/2024-01-02
```

**Response**
```json
{
  "lisboa": {
    "created_at": "2025-10-30 12:22:17.360491", 
    "general_statistics": {
      "days_with_precipitation": 2,
      "end": "2024-01-02",
      "precipitation_max": {
        "date": "2024-01-02T14:00",
        "value": 9.8
      }, 
      "precipitation_total": 16, 
      "start_date": "2024-01-01", 
      "temperature_average": 26.37708333333333, 
      "temperature_max": {
        "date": "2024-01-01T13:00", 
        "value": 32.5
      }, 
      "temperature_min": {
        "date": "2024-01-02T23:00", 
        "value": 22.5
      }
    }, 
    "id": "pl_33.76583_33.76583_2024-01-01_2024-01-02", 
    "precipitation_statistics": {
      "average": 0.4416666666666667, 
      "days_with_precipitation": 2, 
      "max": {
        "date": "2024-01-02T14:00", 
        "value": 9.8
      }, 
      "total": 16, 
      "total_by_day": {
        "2024-01-01": 2.2, 
        "2024-01-02": 19.0
      }
    }, 
    "weather_statistics": {
      "average": 26.37708333333333, 
      "average_by_day": {
        "2024-01-01": 27.483333333333334, 
        "2024-01-02": 25.270833333333332}, 
      "hours_above_threshold": 8, 
      "hours_below_threshold": 0, 
      "max": {
        "date": "2024-01-01T13:00", 
        "value": 32.5
      }, 
      "min": {
        "date": "2024-01-02T23:00", 
        "value": 22.5
      }
    }
  }
}
```

## Testing

### Run All Tests
```bash
 python -m unittest backend.api.tests.test_endpoints  
```

## Development

### Project Structure
```
weather_app/
├── backend/
│   ├── api/
│   │   ├── service/
│   │   │   ├── api_funcs/              # API utility functions
│   │   │   ├── api_open_meteo/         # Third-party API integration
│   │   │   ├── db_manager/             # Database operations
│   │   │   ├── pipeline/               # Data processing pipeline
│   │   │   │   └── functions.py        # Core processing logic
│   │   │   ├── utils/                  # Utility modules
│   │   │   │   └── id_generators.py    # ID generators for DB monitoring
│   │   │   │   └── stats_generator.py  # Module to process weather statistics
│   │   │   │   └── logger.py           # logging monitoring
│   │   │   ├── __init__.py
│   │   │   ├── api.py                  # API helper functions
│   │   │   ├── celery_config.py        # Celery configuration
│   │   │   ├── celery_worker.py        # Celery worker entry point
│   │   │   └── tasks.py                # Celery tasks
│   │   ├── tests/                      # Test suite
│   │   │   ├── cases.py                # Fixed data to test
│   │   │   ├── test_api.py             # Test
│   │   ├── __init__.py
│   │   ├── entrypoint.py               # Container entrypoint
│   │   ├── Dockerfile                  # API container definition
│   │   └── requirements.txt            # Python dependencies
│   ├── database/
│   │   ├── schema/
│   │   │   ├── db_populate.sql      # Initial data
│   │   │   └── schema.sql           # Database schema
│   │   ├── Dockerfile               # Database container
│   │   └── Makefile                 # Database commands
│   ├── init/                        # Initialization scripts
│   │   ├── __init__.py
│   │   ├── Dockerfile
│   │   └── entrypoint.py
│   └── __init__.py
├── logs/                            # Application logs
├── .dockerignore                    # Docker ignore file
├── .env                             # Environment variables
├── .gitignore                       # Git ignore file
├── docker-compose.yml               # Docker orchestration
├── Makefile                         # Development commands
├── requirements.txt                 # Root dependencies
└── README.md                        # This file
```