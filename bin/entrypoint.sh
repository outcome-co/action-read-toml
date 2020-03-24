#! /bin/bash

if [ -v GITHUB_WORKSPACE ]; then
    cd $GITHUB_WORKSPACE
    echo "Switching to Github Workspace: ${GITHUB_WORKSPACE}"
fi

python /app/read_toml.py $@
