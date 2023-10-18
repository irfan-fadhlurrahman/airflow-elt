FROM openjdk:19-buster

ENV MB_PLUGINS_DIR=/home/plugins/

# See for the latest version: https://github.com/AlexR2D2/metabase_duckdb_driver/releases
ADD https://downloads.metabase.com/v1.46.2/metabase.jar /home
ADD https://github.com/AlexR2D2/metabase_duckdb_driver/releases/download/0.8.1/duckdb.metabase-driver.jar /home/plugins/

RUN chmod 744 /home/plugins/duckdb.metabase-driver.jar

CMD ["java", "-jar", "/home/metabase.jar"]
