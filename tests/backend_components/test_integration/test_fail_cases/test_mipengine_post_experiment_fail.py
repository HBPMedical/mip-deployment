import pytest
import json
import time

import requests


def do_get_experiment_request(uuid):
    url = f"http://127.0.0.1:8080/services/experiments/{uuid}"
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    return response


all_error_cases = [
    (
        "Invalid parameter name",
        {
            "algorithm": {
                "name": "LOGISTIC_REGRESSION",
                "label": "Logistic Regression",
                "parameters": [
                    {
                        "name": "xyz",
                        "label": "x",
                        "value": "rightppplanumpolare,righthippocampus,lefthippocampus,rightamygdala,leftamygdala",
                    },
                    {"name": "y", "label": "y", "value": "alzheimerbroadcategory"},
                    {"name": "pathology", "label": "pathology", "value": "dementia"},
                    {"name": "dataset", "label": "dataset", "value": "edsd,ppmi"},
                    {"name": "filter", "label": "filter", "value": ""},
                    {"name": "classes", "label": "classes", "value": "AD,CN"},
                ],
                "type": "mipengine",
            },
            "name": "MIP-Engine Invalid parameter name",
        },
        "text/plain+user_error",
    ),
    (
        "Invalid parameter value",
        {
            "algorithm": {
                "name": "LOGISTIC_REGRESSION",
                "label": "Logistic Regression",
                "parameters": [
                    {"name": "x", "label": "x", "value": "xyz"},
                    {"name": "y", "label": "y", "value": "alzheimerbroadcategory"},
                    {"name": "pathology", "label": "pathology", "value": "dementia"},
                    {"name": "dataset", "label": "dataset", "value": "edsd,ppmi"},
                    {"name": "filter", "label": "filter", "value": ""},
                    {"name": "classes", "label": "classes", "value": "AD,CN"},
                ],
                "type": "mipengine",
            },
            "name": "MIP-Engine Invalid parameter value",
        },
        "text/plain+user_error",
    ),
]


@pytest.mark.parametrize("test_case,test_input,expected_error_type", all_error_cases)
def test_post_request_mip_engine(test_case, test_input, expected_error_type):
    url = "http://127.0.0.1:8080/services/experiments"

    request_json = json.dumps(test_input)

    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(url, data=request_json, headers=headers)
    logistic = json.loads(response.text)
    assert not logistic["shared"]
    assert logistic["status"] == "pending"
    assert test_input["algorithm"]["name"] == logistic["algorithm"]["name"]
    assert test_input["algorithm"]["label"] == logistic["algorithm"]["label"]
    assert test_input["algorithm"]["type"] == logistic["algorithm"]["type"]
    while True:
        logistic_current_state_response = do_get_experiment_request(logistic["uuid"])
        logistic_current_state = json.loads(logistic_current_state_response.text)
        status = logistic_current_state["status"]

        if status != "pending":
            assert status == "error"
            assert expected_error_type == logistic_current_state["result"][0]["type"]
            break
        time.sleep(2)


def test_post_request_mip_engine_invalid_parameter_type():
    url = "http://127.0.0.1:8080/services/experiments"

    request_json = json.dumps(
        {
            "algorithm": {
                "name": "LOGISTIC_REGRESSION",
                "label": "Logistic Regression",
                "parameters": "xyz",
                "type": "mipengine",
            },
            "name": "Error_Logistic_Regression",
        }
    )

    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(url, data=request_json, headers=headers)
    assert "Algorithm: LOGISTIC_REGRESSIO does not exist." in response.text


def test_post_request_mip_engine_invalid_parameter_type():
    url = "http://127.0.0.1:8080/services/experiments"

    request_json = json.dumps(
        {
            "algorithm": {
                "name": "LOGISTIC_REGRESSIO",
                "label": "Logistic Regression",
                "parameters": [
                    {
                        "name": "x",
                        "label": "x",
                        "value": "rightppplanumpolare,righthippocampus,lefthippocampus,rightamygdala,leftamygdala",
                    },
                    {"name": "y", "label": "y", "value": "alzheimerbroadcategory"},
                    {"name": "pathology", "label": "pathology", "value": "dementia"},
                    {"name": "dataset", "label": "dataset", "value": "edsd,ppmi"},
                    {"name": "filter", "label": "filter", "value": ""},
                    {"name": "classes", "label": "classes", "value": "AD,CN"},
                ],
                "type": "mipengine",
            },
            "name": "MIP-Engine Invalid name",
        },
    )

    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(url, data=request_json, headers=headers)
    assert "Algorithm: LOGISTIC_REGRESSIO does not exist." in response.text
