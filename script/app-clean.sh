#!/bin/bash

# Clean `__pycache__/` folders
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

# Clean other folders
rm -rf .mypy_cache/
rm -rf .pytest_cache/
rm -rf .terraform/
rm -rf .venv/
