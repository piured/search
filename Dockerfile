FROM python:3.9-slim-buster

COPY src /opt/src
COPY requirements_inference.txt /opt/requirements_inference.txt
WORKDIR /opt
RUN pip install --no-cache-dir -r requirements_inference.txt

COPY notebooks/distilbert-piu-search/checkpoint-1125 /opt/model

WORKDIR /opt/src/service

ENTRYPOINT [ "python", "main.py", "/opt/model" ]