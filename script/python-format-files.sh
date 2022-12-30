#!/bin/bash

# Format file imports
poetry run isort app

# Format files
poetry run black app
