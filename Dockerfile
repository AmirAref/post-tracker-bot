# pull the images
FROM python:3.11-bullseye

# Set Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Configure Poetry
ENV POETRY_VERSION=1.8.2
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR='/var/cache/pypoetry'
ENV POETRY_HOME='/usr/local'


WORKDIR /code/

# Install Poetry
RUN pip install poetry \
  && poetry --version

# install the dependencies
COPY pyproject.toml ./

RUN poetry install --only main --no-root --no-directory

COPY src/ ./src
RUN poetry install --only main

ENTRYPOINT ["python", "-m", "src.bot"]
