# Juno API

This repository holds the code for the Juno API and scripts for interacting with the docker
containers during development. Juno v1 is a budgeting application and can help track the
progress of various financial goals. The API portion of Juno is written in Python and uses
Postgres for a database.

- [Juno Wiki](https://www.notion.so/Juno-Architecture-aeb7b49391204aee86930adc9a46bf9e?pvs=4)

## Installation

To use this project locally you'll need to check to see if you have Docker on your laptop. Use `docker --version` to see if you have Docker installed. If you do, then this command will show you a Docker version. If you do not have Docker installed then this command will yield an error. [Install docker](https://docs.docker.com/get-docker/s) if you need to.

> `$ docker compose up --build`  
> Starts a server on `http://localhost:8000`

After cloning the repo run `docker compose up --build` from the repo root.
This will create the necessary containers for the API and database and start a docker
environment for Juno. This will start a server on `localhost:8000`.

### Package Management and virtual environment to develop in

Python Poetry creates virtual environments that we can develop in. To create a virtual environment you will need the Poetry CLI.

| Poetry CLI Command | Description                                                      |
| ------------------ | ---------------------------------------------------------------- |
| `poetry install`   | Installs project dependencies and creates a virtual environment. |
| `poetry shell`     | Activates the virtual environment for use.                       |
| `poetry exit`      | Exits the activated virtual environment.                         |

## Project Scripts

After building the project, you can run the commands from the `Command` column in the table
below from the root of this project.

| Command                                  | Description                                                                                                                                                          |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bash scripts/connect_to_postgres`       | This will connect to the PostgreSQL container. Once you have run this command, you can connect to the database by running `psql -U postgres -d postgres`.            |
| `bash scripts/new_migration`             | This can be run after making changes that affect the database. It will prompt you for a short description of the change that the migration file will use for a name. |
| `bash scripts/run_most_recent_migration` | Applies the latest database migration. Typically, this is run after the `new_migration` script. Could probably run this after an initial download                    |

## Documentation

The development of Juno is heavily documented on Confluence. Here are some articles:

- [Creating the test environment infrastructure](https://68thandmaine.atlassian.net/wiki/x/NwA6)
- [Dockerizing the Juno API and Database](https://68thandmaine.atlassian.net/wiki/x/AoB7)