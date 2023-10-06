FROM apache/airflow:slim-2.7.0-python3.11

WORKDIR /opt/airflow
ENV PYTHONPATH=/opt/airflow

ADD /requirements.txt requirements.txt

RUN apt-get update && \
    apt-get install -y wget unzip; \
    pip install -U pip; \
    pip install --no-cache-dir -r requirements.txt
