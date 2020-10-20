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

_gh_arg = '--github-actions'
_check_arg = '--check-only'

_ignore_args = {'', _gh_arg}
_flag_args = {_check_arg}


def get_read_toml_args() -> List[CallArgs]:
    # We need to remove empty strings, because github passes optional
    # parameters as empty strings if not specified
    read_toml_args = []
    for arg in sys.argv[1:]:
        if arg in _ignore_args:
            continue

        arg_clean = arg.lstrip('-').replace('-', '_')
        read_toml_args.append(arg_clean)

        # If the arg is a flag, we inject a 'True' value
        # to be paired with the argument
        if arg in _flag_args:
            read_toml_args.append(True)

    # Group the flags and their values
    # ["--flag", "value", "--other", "other_value"] -> [("--flag", "value"), ("--other", "other_value")]
    arg_pairs = list(zip(*[iter(read_toml_args)] * 2))  # noqa: WPS435

    # Convert to dict
    arg_dict: CallArgs = dict(arg_pairs)

    # If --key contains a new line, then we're reading multiple keys
    key_arg = arg_dict.pop('key', '').strip()
    keys = key_arg.split('\n')

    # Create a list of calls to make to read-toml, one for each key
    args: List[CallArgs] = []

    for key in keys:
        # Create a new call from the provided arguments
        key_args = arg_dict.copy()

        # Make it specific to the key
        key_args['key'] = key.strip()

        args.append(key_args)

    return args


def main():
    """Main function wrapping read-toml."""
    switch_working_directory()

    if _gh_arg in sys.argv:
        write = output_gh
    else:
        write = output

    for call_args in get_read_toml_args():
        key = call_args['key']
        write(key, read_toml.read_toml(**call_args))


def output(key, value):
    console.write(value)


def output_gh(key, value):
    gh_var_key = key.replace('.', '_')
    console.write(f'::set-output name={gh_var_key}::{value}')


if __name__ == '__main__':  # pragma: no cover
    main()
