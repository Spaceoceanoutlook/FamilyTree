FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-root

COPY . .

ENV PYTHONPATH=/app

CMD ["uvicorn", "familytree.main:app", "--host", "0.0.0.0", "--port", "8000"]