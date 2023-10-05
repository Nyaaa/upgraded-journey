FROM python:3.11-alpine

WORKDIR /app

RUN pip install poetry && poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /app/
RUN poetry install -n --no-root --no-cache

COPY ./app /app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]