FROM python:3.10-slim-buster

RUN apt update --no-install-recommends -y

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.13

RUN pip install "poetry==$POETRY_VERSION"

RUN mkdir /polus_hack_back

WORKDIR /polus_hack_back

COPY poetry.lock pyproject.toml /polus_hack_back/

RUN poetry config virtualenvs.create false \
  && poetry install  --no-dev --no-interaction --no-ansi

COPY ./app /polus_hack_back/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
