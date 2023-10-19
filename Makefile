include .env
fix-file-permissions:
	sudo chown -R ${USERNAME} .

create-file:
	mkdir -p ./.github ./tests ./src ./utils ./database
	mkdir -p ./dags ./logs ./plugins 
	mkdir -p ./containers/airflow ./containers/minio/storage ./containers/metabase/metabase-data
	touch .env .gitignore LICENSE.md README.md Makefile compose-dev.yml autostart.sh
	touch ./containers/airflow/Dockerfile
	touch ./containers/airflow/requirements.txt

docker-stats-json:
	docker stats --format "{\"name\":\"{{ .Name }}\",\n\"memory\":{\"raw\":\"{{ .MemUsage }}\",\"percent\":\"{{ .MemPerc }}\"},\n\"cpu\":\"{{ .CPUPerc }}\"}\n"

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
	docker compose --env-file .env -f compose-dev.yml exec airflow-webserver bash

temporary-jupyter: 
	pip install jupyter jupyterlab ipywidgets; \
	jupyter lab --no-browser --ip=0.0.0.0 \
		--port=8877 \
		--allow-root \
		--NotebookApp.token=${JUPYTER_TOKEN} \
		--NotebookApp.disable_check_xsrf=True

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
