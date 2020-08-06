FROM python:3.8 AS build-env

WORKDIR /build

COPY Makefile poetry.lock pyproject.toml ./
COPY make/ ./make/

RUN make generate-production-requirements

RUN pip install -r requirements.txt -t /app/venv

FROM gcr.io/distroless/python3-debian10

COPY --from=build-env /app /app
ENV PYTHONPATH=/app/venv

ADD src/main.py /app/

ENTRYPOINT [ "/usr/bin/python3", "/app/main.py"]
