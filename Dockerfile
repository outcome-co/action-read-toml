FROM python:3.7-alpine

WORKDIR /app

RUN apk add bash

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD ./bin/read_toml.py .
ADD ./bin/entrypoint.sh .

ENTRYPOINT [ "/app/entrypoint.sh" ]
