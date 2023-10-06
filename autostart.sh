#!/bin/bash
/bin/sleep 5

# Ensure the environment is available
source $HOME/.bashrc
source $HOME/.profile

# APScheduler
SESSION_NAME=airflow-metabase
DIRECTORY_PATH="cd $HOME/airflow-elt"
STOP="docker compose --env-file .env -f compose-dev.yml down --remove-orphans"
START="docker compose --env-file .env -f compose-dev.yml up"
SCRIPT_TO_RUN="${DIRECTORY_PATH}; ${STOP}; ${START}"
/usr/bin/tmux set-option -g default-shell /bin/bash
/usr/bin/tmux new-session -ds $SESSION_NAME "source $HOME/.bashrc; source $HOME/.profile; $SCRIPT_TO_RUN; bash"