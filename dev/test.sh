#!/bin/env bash

echo -n "Installing pip requirements ..."
pip install -r requirements.txt

echo -n "Running tests..."
pytest -k "not test_federation_info.py" tests
pytest tests/test_federation_info.py

