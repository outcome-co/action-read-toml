FROM python:3.8.7 AS build-env

WORKDIR /build

COPY Makefile poetry.lock pyproject.toml ./
COPY make/ ./make/

RUN make generate-production-requirements

RUN pip install -r requirements.txt --no-cache-dir -t /app/venv

# Distroless don't currently have version tags
FROM gcr.io/distroless/python3-debian10@sha256:33ddd28c748279670ad4d7ca9ad088c233f2f7bef6daf0a6ed00fc89490dffce

COPY --from=build-env /app /app
ENV PYTHONPATH=/app/venv

COPY src/main.py /app/

ENTRYPOINT [ "/usr/bin/python3", "/app/main.py"]
