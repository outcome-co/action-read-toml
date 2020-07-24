#! /usr/bin/env python3

import sys
import toml
import click
import os


_scalar_types = [int, str, bool, float]


@click.command()
@click.option("--path", help="The path to the TOML file", required=True, type=click.File("r"))
@click.option("--key", help="The path to read from the TOML file", required=True)
def read_toml(path, key: str):
    """
    Reads the value specified by the path from a TOML file.
    The path parameter should be a '.' separated sequences of keys
    that correspond to a path in the TOML structure.

    Example TOML file:

    ---
    title = "My TOML file"

    [info]
    version = "1.0.1"

    [tools.poetry]
    version = "1.1.2"
    files = ['a.py', 'b.py']
    ---

    Read standard keys:

    read_toml.py --path my_file.toml --key title -> "My TOML file"
    read_toml.py --path my_file.toml --key info.version -> "1.0.1"

    Read arrays:

    read_toml.py --path my_file.toml --key tools.poetry.files -> "a.py b.py"

    Read non-leaf keys:

    read_toml.py --path my_file.toml --key tools -> #ERROR
    """

    def fail():
        print(f"Invalid key: {key}", file=sys.stderr)
        sys.exit(-1)

    def output(value: str):
        if os.environ.get('GITHUB_ACTIONS', False):
            action_key = key.replace('.', '_')
            print(f"::set-output name={action_key}::{value}")
        else:
            print(value)

    try:
        value = _read_path(path, key)
    except KeyError:
        fail()

    # Just print scalars
    if type(value) in _scalar_types:
        output(value)

    elif isinstance(value, list):
        output(" ".join(value))

    # We could theoretically just print out the dict, but we'll fail instead
    else:
        fail()


def _read_path(path, key: str):
    parsed_toml = toml.loads(path.read())
    keys = key.split(".")
    keys.reverse()

    node = parsed_toml

    while keys:
        _key = keys.pop()

        # If we still have keys left, and the current node isn't a dict
        # that's an invalid path
        if not isinstance(node, dict):
            raise KeyError

        # This will also throw a KeyError if key isn't available in node
        node = node[_key]

    return node


if __name__ == "__main__":
    # If we're in a Github Action, the GITHUB_WORKSPACE variable
    # will be set, and corresponds to the directory mounted as a volume
    # in the Docker.
    #
    # Since we're likely to be working on the files in the GITHUB_WORKSPACE
    # we automatically change directories
    if 'GITHUB_WORKSPACE' in os.environ:
        workspace = os.environ['GITHUB_WORKSPACE']
        print(f'Switching to Github Workspace: {workspace}')
        os.chdir(workspace)

    read_toml()
