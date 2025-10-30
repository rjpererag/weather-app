#!/bin/bash

# Check if .env file already exists
if [ -f ".env" ]; then
    echo ".env file already exists. Skipping creation."
    exit 0
fi

echo "Creating .env file with default values..."

cat << EOF > .env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0

DATABASE_URL=postgresql://your_user:your_password@db:5432/weather_db

EOF
echo ".env file created successfully."