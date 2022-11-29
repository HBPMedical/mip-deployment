#!/bin/env bash

cd backend_components/test_integration/
poetry run pytest test_success_cases/

poetry run pytest test_fail_cases/

poetry run pytest test_federation_info.py

cd ../../

