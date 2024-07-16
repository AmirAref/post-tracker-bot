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
# https://github.com/python-poetry/poetry
RUN curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version


# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# install the dependencies
COPY pyproject.toml ./

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-dev --no-root ; fi"


COPY src/ ./src

ENTRYPOINT ["python", "-m", "src.bot"]
