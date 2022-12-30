#!/bin/bash

# Initialize terraform
terraform init

# Install python dependencies
poetry install --no-root
