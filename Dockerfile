FROM python:3.11-alpine
WORKDIR /usr/src/app
RUN pip install poetry && poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml .env /usr/src/app/
RUN poetry install -n --no-root --only main --no-cache
COPY ./FSTR /usr/src/app/