FROM python:3.13.0-slim

# Set work directory
WORKDIR /app/backend-api

COPY pyproject.toml /app/backend-api/

RUN pip3 install --upgrade pip \
&& pip3 install poetry \
&& poetry config virtualenvs.in-project true \
&& poetry install

# Activate the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

RUN apt-get update  -y \
    && apt-get clean

RUN apt-get install make

COPY . /app/backend-api/
