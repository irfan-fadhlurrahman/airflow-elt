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

up: down
	docker compose --env-file .env -f compose-dev.yml up

up-with-rebuild: down
	docker compose --env-file .env -f compose-dev.yml up --build

down:
	docker compose --env-file .env -f compose-dev.yml down

down-remove-orphans:
	docker compose --env-file .env -f compose-dev.yml down --remove-orphans

bash:
	docker compose --env-file .env -f compose-dev.yml exec airflow-webserver bash

attach:
	tmux a -t airflow-metabase

kill:
	tmux kill-session -t airflow-metabase

autostart:
	chmod +x ./autostart.sh && . ./autostart.sh

restart: kill autostart

rebuild: down-remove-orphans kill build autostart attach

prune:
	docker builder prune -a
	docker image prune -a

git-pull:
	git add .
	git commit -m "to update the latest repo"
	git pull origin main
