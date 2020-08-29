#! /usr/bin/env python3

"""A utility to read values from TOML files."""

import os
import sys

from outcome.read_toml import bin as read_toml
from outcome.utils import console


def switch_working_directory():
    # If we're in a Github Action, the GITHUB_WORKSPACE variable
    # will be set, and corresponds to the directory mounted as a volume
    # in the Docker.
    #
    # Since we're likely to be working on the files in the GITHUB_WORKSPACE
    # we automatically change directories
    workspace = os.environ.get('GITHUB_WORKSPACE')
    if workspace:
        console.write(f'Switching to Github Workspace: {workspace}')
        os.chdir(workspace)


def get_read_toml_args():
    # We need to remove empty strings, because github passes optionnal
    # parameter as empty string if not specified
    read_toml_args = [arg for arg in sys.argv[1:] if arg != '']
    # If we are in Github Actions we add --github-actions arg to format output accordingly
    if os.environ.get('GITHUB_ACTIONS', False):
        read_toml_args += ['--github-actions']
    return read_toml_args


def main():
    """Main function wrapping read-toml."""
    switch_working_directory()
    read_toml_args = get_read_toml_args()
    read_toml.read_toml(read_toml_args)


if __name__ == '__main__':  # pragma: no cover
    main()
