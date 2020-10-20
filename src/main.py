#! /usr/bin/env python3

"""A utility to read values from TOML files."""

import os
import sys
from typing import Dict, List, Union

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


CallArgs = Dict[str, Union[str, bool]]


def get_read_toml_args() -> List[CallArgs]:
    # We need to remove empty strings, because github passes optional
    # parameters as empty strings if not specified
    read_toml_args = [arg.lstrip('-').replace('-', '_') for arg in sys.argv[1:] if arg != '']
    # If we are in Github Actions we add --github-actions arg to format output accordingly

    # Group the flags and their values
    # ["--flag", "value", "--other", "other_value"] -> [("--flag", "value"), ("--other", "other_value")]
    arg_pairs = list(zip(*[iter(read_toml_args)] * 2))  # noqa: WPS435

    # Convert to dict
    arg_dict: CallArgs = dict(arg_pairs)

    if os.environ.get('GITHUB_ACTIONS', False):
        arg_dict['github_actions'] = True

    # If --key contains a new line, then we're reading multiple keys
    key_arg = arg_dict.pop('key', '').strip()
    keys = key_arg.split('\n')

    # Create a list of calls to make to read-toml, one for each key
    args: List[CallArgs] = []

    for key in keys:
        # Create a new call from the provided arguments
        key_args = arg_dict.copy()

        # Make it specific to the key
        key_args['key'] = key

        args.append(key_args)

    return args


def main():
    """Main function wrapping read-toml."""
    switch_working_directory()

    for call_args in get_read_toml_args():
        read_toml.read_toml(**call_args)


if __name__ == '__main__':  # pragma: no cover
    main()
