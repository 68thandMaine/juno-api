#!/bin/bash

# Prompt the user for a breif description of the changes
echo "Describe the change in five words or less?"
read description

docker compose exec api alembic revision --autogenerate -m "$description"
docker compose exec api alembic upgrade head