FROM python:3.9-slim as base

WORKDIR /usr/src/mock_server

COPY docker/Pipfile .
RUN pip install pipenv

# 開発用
FROM base as dev
RUN pipenv install --dev

# 本番用
FROM base as prod
RUN pipenv install
COPY backend backend