# syntax=docker/dockerfile:1
FROM python:3.9 as requirements-stage

WORKDIR /tmp

RUN pip3 install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9.4

WORKDIR /usr/src/juno_api

COPY --from=requirements-stage /tmp/requirements.txt /usr/src/juno_api/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# ARG GITLAB_TOKEN=""
# ARG GITLAB_TOKEN_USERNAME=""

# RUN pip3 install  git+https://${GITLAB_TOKEN_USERNAME}:${GITLAB_TOKEN}@gitlab.absci.cloud/informatics/unlimiter.git@v1.0.0

COPY . /usr/src/juno_api
