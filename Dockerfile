FROM python:3.10.11-bullseye as base 
WORKDIR  /juno_api

COPY /pyproject.toml /juno_api

# don't create .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# disable buffering; recommended when running in a container
ENV PYTHONUNBUFFERED 1
ENV PYTHONUTF8 1

RUN pip3 install --upgrade pip>=23.0.1
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install 

COPY . ./juno_api

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]
