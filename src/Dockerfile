FROM python:3.11.0-alpine

WORKDIR /usr/src/app

RUN pip install poetry && poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /usr/src/app/
RUN poetry install -n --no-root --no-cache

COPY ./src/app /usr/src/app/