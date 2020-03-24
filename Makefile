APP_NAME = action-read-toml
APP_VERSION = $(shell cat VERSION)

DOCKER_NAMESPACE = outcomeco
DOCKER_REPOSITORY= $(DOCKER_NAMESPACE)/$(APP_NAME)

.PHONY: docker-build docker-run docker-clean docker-publish docker-info

docker-build:
	docker build -t $(DOCKER_REPOSITORY):$(APP_VERSION) .
	docker tag $(DOCKER_REPOSITORY):$(APP_VERSION) $(DOCKER_REPOSITORY):latest

docker-clean:
	docker image rm $(DOCKER_REPOSITORY)

docker-publish: docker-build
	docker push $(DOCKER_REPOSITORY):$(APP_VERSION)
	docker push $(DOCKER_REPOSITORY):latest

docker-info:
	@echo ::set-output name=docker_repository::$(DOCKER_REPOSITORY)
	@echo ::set-output name=docker_tag::$(APP_VERSION)
