APP_NAME = action-read-toml
APP_VERSION = $(shell cat VERSION)

.PHONY: docker-build docker-run docker-clean

docker-build:
	docker build -t $(APP_NAME):$(APP_VERSION) .
	docker tag $(APP_NAME):$(APP_VERSION) $(APP_NAME):latest


docker-clean:
	docker image rm $(APP_NAME)
