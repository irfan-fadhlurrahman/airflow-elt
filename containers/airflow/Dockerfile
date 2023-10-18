FROM apache/airflow:slim-2.7.0-python3.11

USER root
RUN apt-get update && \
    apt-get install -y \
        wget unzip zip \
        gconf-service libasound2 libatk1.0-0 libcairo2 \
        libcups2 libfontconfig1 libgdk-pixbuf2.0-0 \
        libgtk-3-0 libnspr4 libpango-1.0-0 libgbm1 \
        libxss1 fonts-liberation libappindicator1 \
        libnss3 lsb-release libu2f-udev xdg-utils; \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb; \ 
    sudo dpkg -i google-chrome-stable_current_amd64.deb; \
    apt-get -fy install;

WORKDIR /opt/airflow
ENV PYTHONPATH=/opt/airflow

ADD /requirements.txt requirements.txt

USER airflow
RUN pip install -U pip; \
    pip install -r requirements.txt --no-cache-dir
