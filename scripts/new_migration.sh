#!/bin/bash

# Prompt the user for their name
echo "Describe the change in five words or less?"
read description

docker compose exec api alembic revision --autogenerate -m "$description"
