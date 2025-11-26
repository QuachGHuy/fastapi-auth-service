# BASE
FROM python:3.10-slim AS base

WORKDIR /auth-api

RUN apt-get update \
    && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# DEVLOPMENT
FROM python:3.10-slim AS dev

WORKDIR /auth-api

RUN apt-get update \
    && apt-get install -y \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=base /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# PRODUCTION
FROM python:3.10-slim AS prod

WORKDIR /auth-api

RUN apt-get update \
    && apt-get install -y libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=base /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY . .

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]