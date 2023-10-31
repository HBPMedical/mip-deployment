#!/bin/env bash

pytest -k "not test_federation_info.py" tests
pytest tests/test_federation_info.py

