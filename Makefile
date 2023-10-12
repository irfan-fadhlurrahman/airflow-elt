include .env

create-file:
	mkdir -p ./.github ./tests ./src ./utils ./database
	mkdir -p ./dags ./logs ./plugins 
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

up-with-rebuild: down-remove-orphans
	docker compose --env-file .env -f compose-dev.yml up --build

down:
	docker compose --env-file .env -f compose-dev.yml down

down-remove-orphans:
	docker compose --env-file .env -f compose-dev.yml down --remove-orphans

bash:
	docker compose --env-file .env -f compose-dev.yml exec airflow-scheduler bash

attach:
	tmux a -t ${TMUX_SESSION_NAME}

kill:
	tmux kill-session -t ${TMUX_SESSION_NAME}

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

git-push:
	git push origin main


unit-test:
	pytest tests/unit/test_utils_common.py -s --disable-warnings
