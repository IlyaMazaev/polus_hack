FROM python:3.10-slim-buster



RUN pip install fastapi uvicorn

RUN mkdir /polus_hack_back

WORKDIR /polus_hack_back

COPY ./app /polus_hack_back/app

COPY requirements.txt /polus_hack_back/requirements.txt

RUN pip install -r requirements.txt


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
