#! /usr/bin/env python3

"""A utility to read values from TOML files."""

import inspect
import os
from pathlib import Path

import makefun
import typer
from outcome.read_toml import bin as read_toml
from outcome.utils import console


def run(github_actions: bool, key: str, *args, **kwargs):
    if github_actions:
        switch_working_directory()

    if github_actions:
        write = output_gh
    else:
        write = output

    keys = key.strip().split('\n')

    for k in keys:
        write(k, read_toml.read_toml(key=k, *args, **kwargs))


def output(key, value):
    console.write(value)


def output_gh(key, value):
    gh_var_key = key.replace('.', '_').replace('-', '_')
    console.write(f'::set-output name={gh_var_key}::{value}')


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


def build():
    app = typer.Typer()

    signature = inspect.signature(read_toml.read_toml)

    # Typer doesn't handle Union types
    # Remove the path parameter, which is of type Union[IO[str], str, Path]
    # Replace it with path of type Path

    # We'll also replace the key parameter with a parameter with typer.Option(...) as a default value
    # which makes it behave like a required option: https://typer.tiangolo.com/tutorial/options/required/
    # This is necessary to have the same interface as the underlying read-toml CLI
    signature = makefun.remove_signature_parameters(signature, 'path', 'key')
    params = list(signature.parameters.values())

    path_parameter = inspect.Parameter(
        'path', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=Path, default=typer.Option(...),
    )
    params.insert(0, path_parameter)

    key_parameter = inspect.Parameter(
        'key', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=str, default=typer.Option(...),
    )
    params.insert(0, key_parameter)

    github_parameter = inspect.Parameter('github_actions', kind=inspect.Parameter.KEYWORD_ONLY, default=False, annotation=bool)
    params.append(github_parameter)

    signature = signature.replace(parameters=params)

    @app.command()
    @makefun.wraps(read_toml.read_toml, new_sig=signature)
    def read_toml_cli(*args, **kwargs):
        run(*args, **kwargs)

    return app  # noqa: R504


if __name__ == '__main__':  # pragma: no cover
    app = build()
    app()
