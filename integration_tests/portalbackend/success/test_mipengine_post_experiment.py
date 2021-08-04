import pytest
import json
import time

import requests


def do_get_experiment_request(uuid):
    url = f"http://127.0.0.1:8080/services/experiments/{uuid}"
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    return response


all_success_cases = [
    {
        "algorithm": {
            "name": "LOGISTIC_REGRESSION",
            "label": "Logistic Regression",
            "parameters": [
                {
                    "name": "x",
                    "label": "x",
                    "value": "rightppplanumpolare,righthippocampus,lefthippocampus,rightamygdala,leftamygdala"
                },
                {
                    "name": "y",
                    "label": "y",
                    "value": "alzheimerbroadcategory"
                },
                {
                    "name": "pathology",
                    "label": "pathology",
                    "value": "dementia"
                },
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "edsd,ppmi"
                },
                {
                    "name": "filter",
                    "label": "filter",
                    "value": ""
                },
                {
                    "name": "classes",
                    "label": "classes",
                    "value": "AD,CN"
                }
            ],
            "type": "mipengine"
        },
        "name": "Logistic_Regression"
    },
    {
        "algorithm": {
            "name": "LOGISTIC_REGRESSION",
            "label": "Logistic Regression",
            "parameters": [
                {
                    "name": "x",
                    "label": "x",
                    "value": "rightbasalforebrain,leftbasalforebrain,rightaccumbensarea,leftaccumbensarea,rightpallidum,leftpallidum,rightcaudate,rightputamen,leftcaudate,leftputamen,rightamygdala,leftamygdala"
                },
                {
                    "name": "y",
                    "label": "y",
                    "value": "parkinsonbroadcategory"
                },
                {
                    "name": "pathology",
                    "label": "pathology",
                    "value": "dementia"
                },
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "edsd,ppmi"
                },
                {
                    "name": "filter",
                    "label": "filter",
                    "value": ""
                },
                {
                    "name": "classes",
                    "label": "classes",
                    "value": "PD,CN"
                }
            ],
            "type": "mipengine"
        },
        "name": "Big One"
    }
]


@pytest.mark.parametrize(
    "test_input", all_success_cases
)
def test_post_request_mip_engine(test_input):

    url = "http://127.0.0.1:8080/services/experiments"

    print(f"POST to {url}")
    request_json = json.dumps(test_input)

    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(url, data=request_json, headers=headers)

    print(f"POST MIP-ENGINE result-> {response.text}")
    logistic = json.loads(response.text)
    assert logistic["algorithm"]["name"] == "LOGISTIC_REGRESSION"
    assert not logistic["shared"]
    assert logistic["status"] == "pending"
    assert test_input["algorithm"]["name"] == logistic["algorithm"]["name"]
    assert test_input["algorithm"]["label"] == logistic["algorithm"]["label"]
    assert test_input["algorithm"]["type"] == logistic["algorithm"]["type"]
    while True:
        logistic_curent_state_response = do_get_experiment_request(logistic["uuid"])
        logistic_curent_state = json.loads(logistic_curent_state_response.text)
        status = logistic_curent_state["status"]
        print(status)
        if status != "pending":
            assert status == "success"
            assert logistic_curent_state["result"] is not None
            break
        time.sleep(2)
