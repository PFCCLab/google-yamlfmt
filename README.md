# google-yamlfmt

A PyPI packaging repository for [yamlfmt](https://github.com/google/yamlfmt), making it easily accessible to the Python ecosystem.

## Overview

This repository provides a Python package wrapper for Google's `yamlfmt` tool, enabling seamless integration with Python package managers and development workflows. The original `yamlfmt` is a powerful YAML formatter written in Go, and this package makes it available through PyPI for easier installation and use in Python projects.

## Features

- **Easy Installation**: Install via pip or any Python package manager
- **Python Ecosystem Integration**: Works seamlessly with Python development workflows
- **Pre-commit Support**: Perfect for use with pre-commit hooks
- **Cross-platform**: Available on all platforms supported by the original yamlfmt

## Installation

To install google-yamlfmt, ensure you have Python 3.9 or higher, then run:

```bash
pip install google-yamlfmt
```

## Usage

After installation, you can format YAML files using the `yamlfmt` command:

```bash
yamlfmt <file_or_directory>
```

Examples:

```bash
# Format a single file
yamlfmt example.yaml

# Format multiple files
yamlfmt file1.yaml file2.yaml

# Format all YAML files in current directory
yamlfmt *.yaml

# Check if files need formatting (lint mode)
yamlfmt -lint example.yaml
```

For more advanced usage options and configuration, please refer to the [original documentation](https://github.com/google/yamlfmt/blob/main/docs/command-usage.md) or run `yamlfmt -h`.

### Pre-commit Integration

To use with pre-commit, add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/PFCCLab/yamlfmt-pre-commit-mirror.git
    rev: v0.17.2
    hooks:
      - id: yamlfmt
```

## About

This package is a redistribution of the original [yamlfmt](https://github.com/google/yamlfmt) tool created by Google. All credit for the core functionality goes to the original maintainers. This packaging effort aims to make the tool more accessible to Python developers and integrate better with Python-based development workflows.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to help improve this packaging and distribution effort.
