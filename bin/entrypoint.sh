#! /bin/bash

# If we're in a Github Action, the GITHUB_WORKSPACE variable
# will be set, and corresponds to the directory mounted as a volume
# in the Docker.
#
# Since we're likely to be working on the files in the GITHUB_WORKSPACE
# we automatically change directories
if [ -v GITHUB_WORKSPACE ]; then
    cd $GITHUB_WORKSPACE
    echo "Switching to Github Workspace: ${GITHUB_WORKSPACE}"
fi

# The $@ passes all of the arguments passed to ./entrypoint.sh
# to the python script
#
# ./entrypoint.sh --key my.key --path myfile.toml
#
# -> python /app/read_toml.py --key my.key --path myfile.toml
python /app/read_toml.py $@
