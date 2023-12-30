#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE juno_db_test;
    GRANT ALL PRIVILEGES ON DATABASE juno_db_test TO postgres;
EOSQL
