#!/bin/bash

# Wait for the Postgres Docker container
# Replace 'postgres' and '5432' with your Postgres host and port if they're different
while ! nc -z postgres 5432; do
  sleep 1
done

# Init the database
airflow db init
airflow users create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
airflow scheduler & airflow webserver

