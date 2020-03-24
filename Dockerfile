FROM python:3.7-alpine

WORKDIR /app

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD ./bin/read_toml.py .

ENTRYPOINT [ "/app/read_toml.py" ]
