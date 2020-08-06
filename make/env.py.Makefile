ifndef MK_ENV_PY
MK_ENV_PY=1

# We want to define READ_PYPROJECT_KEY in order to read configuration variables from pyproject.toml
# If we are in an environment with python installed we want to use local read-toml
# On the other hand, if we can't install it, we want to use docker image action-read-toml instead

HAS_LOCAL_READ_TOML = $(shell which read-toml 2> /dev/null || echo -1)

ifneq ($(HAS_LOCAL_READ_TOML),-1)
# Environment has read-toml installed, use it to read pyroject.toml
$(info Use local read-toml to read pyproject.toml)
READ_PYPROJECT_KEY=read-toml --path pyproject.toml --key
else
$(info Try to install read-toml)
# Environment has not read-toml installed, try to install it
INSTALL_READ_TOML := $(shell pip install --no-cache --upgrade outcome-read-toml 2> /dev/null || echo -1)
# Test if read-toml is properly installed
# Sadly this test is necessary in github environment, where installation can be successful, but then read-toml is not found
# if python is not properly configured
TEST_INSTALLED_READ_TOML = $(shell read-toml --help 2> /dev/null || echo -1)
ifneq ($(TEST_INSTALLED_READ_TOML),-1)
$(info Use installed read-toml to read pyproject.toml)
READ_PYPROJECT_KEY=read-toml --path pyproject.toml --key
else
$(info Installation failed, check if docker is installed)
# Installation of Read Toml failed, check if environment has docker instead
HAS_DOCKER = $(shell which docker 2> /dev/null || echo -1)
ifeq ($(HAS_DOCKER),-1)
# Environment has not docker installed, we cannot use action-read-toml 
$(error Cannot use read-toml in the environment)
else
# Environment has docker installed, use action-read-toml docker image
$(info Use docker image action-read-toml to read pyproject.toml)
READ_PYPROJECT_KEY=docker run --rm -v $$(pwd):/work/ outcomeco/action-read-toml:latest --path /work/pyproject.toml --key
endif
endif
endif

endif
