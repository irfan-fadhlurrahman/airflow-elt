## Issues

1. Environment flags bug in the docker compose
* Date:
  * October 18th, 2023
* Known bugs: 
    * --env-file flags is ignore if you specify environemnt in docker-compose.yml. 
* Solved by:
    * stated all .env variables at environment on the docker-compose.yml services.
* Reference: 
    * https://stackoverflow.com/questions/48495663/docker-compose-env-file-not-working


2. Use DuckDB on the Metabase
* Date:
  * October 18th, 2023
* Known bugs:
  * No DuckDB JDBC driver on the Metabase Dockerfile.
* Solved by:
  * Create custom Dockerfile to add DuckDB JDBC driver.
* Reference:
  * https://github.com/AlexR2D2/metabase_duckdb_driver
    
