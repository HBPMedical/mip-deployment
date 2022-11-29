#!/bin/env bash

cd backend_components/test_integration/
pytest test_success_cases/

pytest test_fail_cases/

pytest test_federation_info.py

cd ../../

