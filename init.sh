#!/bin/bash
mkdir -p ./.github
mkdir -p ./dags ./logs ./plugins ./test ./src ./utils
mkdir -p ./containers/airflow ./containers/minio/storage
touch .env .gitignore LICENSE.md README.md Makefile compose-dev.yml autostart.sh
touch ./containers/airflow/Dockerfile
touch ./containers/airflow/requirements.txt