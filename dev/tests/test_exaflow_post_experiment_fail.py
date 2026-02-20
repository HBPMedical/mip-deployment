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
                "name": "logistic_regression",
                "parameters": [
                    {
                        "name": "xyz",
                        "value": "rightppplanumpolare,righthippocampus,lefthippocampus,rightamygdala,leftamygdala",
                    },
                    {"name": "y", "value": "alzheimerbroadcategory"},
                    {"name": "pathology", "value": "dementia"},
                    {"name": "dataset", "value": "edsd,ppmi"},
                    {"name": "filter", "value": ""},
                    {"name": "positive_class", "value": "AD,CN"},
                ],
            },
            "name": "Exaflow Invalid parameter name",
        },
        "text/plain+user_error",
    ),
    (
        "Invalid algorithm name",
        {
            "algorithm": {
                "name": "LOGISTIC_REGRESSION",
                "parameters": [
                    {
                        "name": "xyz",
                        "value": "rightppplanumpolare,righthippocampus,lefthippocampus,rightamygdala,leftamygdala",
                    },
                    {"name": "y", "value": "alzheimerbroadcategory"},
                    {"name": "pathology", "value": "dementia"},
                    {"name": "dataset", "value": "edsd,ppmi"},
                    {"name": "filter", "value": ""},
                    {"name": "positive_class", "value": "AD,CN"},
                ],
            },
            "name": "Exaflow Invalid parameter name",
        },
        "text/plain+error",
    ),
    (
        "Invalid parameter value",
        {
            "algorithm": {
                "name": "logistic_regression",
                "parameters": [
                    {"name": "x", "value": "xyz"},
                    {"name": "y", "value": "alzheimerbroadcategory"},
                    {"name": "pathology", "value": "dementia"},
                    {"name": "dataset", "value": "edsd,ppmi"},
                    {"name": "filter", "value": ""},
                    {"name": "positive_class", "value": "AD,CN"},
                ],
            },
            "name": "Exaflow Invalid parameter value",
        },
        "text/plain+user_error",
    ),
]


@pytest.mark.parametrize("test_case,test_input,expected_error_type", all_error_cases)
def test_post_request_exaflow(test_case, test_input, expected_error_type):
    url = "http://127.0.0.1:8080/services/experiments"

    request_json = json.dumps(test_input)

    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(url, data=request_json, headers=headers)
    logistic = json.loads(response.text)
    assert not logistic["shared"]
    assert logistic["status"] == "pending"
    assert test_input["algorithm"]["name"] == logistic["algorithm"]["name"]

    while True:
        logistic_current_state_response = do_get_experiment_request(logistic["uuid"])

        logistic_current_state = json.loads(logistic_current_state_response.text)
        status = logistic_current_state["status"]

        if status != "pending":
            assert status == "error"
            if "result" in logistic_current_state:
                assert expected_error_type == logistic_current_state["result"][0]["type"]
            break
        time.sleep(2)


def test_post_request_exaflow_invalid_parameters_type():
    url = "http://127.0.0.1:8080/services/experiments"

    request_json = json.dumps(
        {
            "algorithm": {
                "name": "LOGISTIC_REGRESSION",
                "parameters": "xyz",
            },
            "name": "Error_Logistic_Regression",
        }
    )

    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(url, data=request_json, headers=headers)
    assert response.status_code == 400
