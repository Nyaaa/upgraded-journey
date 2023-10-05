FROM python:3.11-alpine

WORKDIR /app

RUN pip install poetry && poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /app/
RUN poetry install -n --no-root --no-cache

COPY ./app /app/
ENTRYPOINT ["./app/docker-entrypoint.sh"]