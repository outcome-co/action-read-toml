ifndef MK_VARS_DOCKER_PY
MK_VARS_DOCKER_PY=1

include make/env.Makefile

DOCKER_REGISTRY = $(shell $(READ_PYPROJECT_KEY) tool.docker.registry)
DOCKER_REPOSITORY = $(shell $(READ_PYPROJECT_KEY) tool.docker.repository)

endif
