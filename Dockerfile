FROM python:3-slim AS build-env
ADD requirements.txt /build/
WORKDIR /build

ADD ./bin/read_toml.py /app/
RUN pip install -r requirements.txt -t /app/venv

FROM gcr.io/distroless/python3-debian10

COPY --from=build-env /app /app
ENV PYTHONPATH=/app/venv
ENTRYPOINT [ "/usr/bin/python3", "/app/read_toml.py"]
