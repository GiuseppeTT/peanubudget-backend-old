# Based on: https://fastapi.tiangolo.com/deployment/docker/#docker-image-with-poetry

# Select python version
ARG VARIANT=3.11

# Generate `requirements.txt`
FROM python:${VARIANT} as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Install python dependencies and copy app
FROM python:${VARIANT}

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
