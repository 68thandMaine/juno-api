#!/bin/bash

# Load the most recent db migration.

docker compose exec api alembic upgrade head