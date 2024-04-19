FROM python:3.11-slim-buster
 
WORKDIR /backend
 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
 
# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean
 
# install python dependencies
RUN pip install --upgrade pip

RUN pip install poetry==1.8.2

ENV\
    POETRY_VIRTUALENVS_CREATE=false\
    POETRY_VITRUALENV_IN_PROJECT=false\
    POETRY_NO_INTERACTION=1\
    POETRY_VERSION=1.8.2

COPY poetry.lock pyproject.toml ./

RUN poetry install
 
COPY . /backend
 
 