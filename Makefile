include .env

create-file:
	mkdir -p ./.github
	mkdir -p ./dags ./logs ./plugins ./tests ./src ./utils
	mkdir -p ./containers/airflow ./containers/minio/storage ./containers/metabase/metabase-data
	touch .env .gitignore LICENSE.md README.md Makefile compose-dev.yml autostart.sh
	touch ./containers/airflow/Dockerfile
	touch ./containers/airflow/requirements.txt

create-docker-network:
	docker network create ${DOCKER_NETWORK}

build:
	docker compose --env-file .env -f compose-dev.yml build