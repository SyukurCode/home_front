# syntax=docker/dockerfile:1

FROM python:3.10.12-slim-buster

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN mkdir /app/logs
RUN touch /app/logs/gui.log

COPY . .

CMD [ "python3", "index.py"]
