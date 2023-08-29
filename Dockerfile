FROM python:3.9-slim-buster

COPY notebooks/distilbert-piu-search/checkpoint-6094 /opt/model
COPY src /opt/src
COPY requirements_inference.txt /opt/requirements_inference.txt

WORKDIR /opt

RUN pip install -r requirements_inference.txt
WORKDIR /opt/src/service

ENTRYPOINT [ "python", "main.py", "/opt/model" ]