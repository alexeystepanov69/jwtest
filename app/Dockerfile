FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apt-get update && apt-get install -y netcat libreoffice-calc docker.io --no-install-recommends --no-install-suggests

COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt