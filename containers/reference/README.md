## Issues

1. Environment flags bug in the docker compose
Known bugs: 
    --env-file flags is ignore if you specify environemnt in docker-compose.yml. 
Solved by:
    stated all .env variables at environment on the docker-compose.yml services.
Reference: 
    https://stackoverflow.com/questions/48495663/docker-compose-env-file-not-working