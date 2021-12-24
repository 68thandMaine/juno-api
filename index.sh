#!/bin/bash
echo $' '  
echo $'Starting the Docker Container for the Juno API'
echo $'\n--------------------------\n'
docker-compose -f docker-compose.yaml --env-file .env up -d --build

echo $'Logs:\n'
docker-compose logs -f -t juno_api
