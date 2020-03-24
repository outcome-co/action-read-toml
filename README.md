# action-read-toml
![ci-badge](https://github.com/outcome-co/action-read-toml/workflows/Continuous%20Integration/badge.svg)

A Github Action to read a specified key from a TOML file and store it in a step output.

## Usage

Given the following TOML file:
```toml
title = "My TOML file"

[info]
version = "1.0.1"

[tools.poetry]
version = "1.1.2"
files = ['a.py', 'b.py']
```

You can use the action to read a key from the file.

```yaml
- uses: outcome-co/action-read-toml@master
    with:
        # Read the specified TOML file
        path: $GITHUB_WORKSPACE/sample.toml
        
        # Read the key
        key: info.version
```

### Output name
The output name will be the key, with `.` replaced by `_` to avoid conflicts in the Github Expression syntax.

### Example

You can find this (example in this repository)[https://github.com/outcome-co/action-read-toml/actions?query=workflow%3A%22Sample+Execution%22].

```yaml
name: Sample Execution

on: push

jobs:
    test_toml:
      name: "Read TOML Sample"
      runs-on: ubuntu-latest
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}"
      steps:
        - name: "Check out code"
          uses: actions/checkout@v2
          with:
            fetch-depth: 0
  
        - name: "Read TOML"
          id: read_toml
          uses: ./
          with:
            path: sample.toml
            key: info.version

        - name: "Print output"
          run: echo ${{ steps.read_toml.outputs.info_version }}
```

## Development

Remember to run `./pre-commit.sh` when you clone the repository.
