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
                    "value": "dementia:0.1"
                },
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "edsd0,edsd1,edsd8,edsd9,ppmi0,ppmi1,ppmi8,ppmi9"
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
        "name": "Logistic small"
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
                    "value": "dementia:0.1"
                },
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "edsd0,edsd1,edsd8,edsd9,ppmi0,ppmi1,ppmi8,ppmi9"
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
        "name": "Logistic big"
    },
    {
        "algorithm": {
            "name": "PCA",
            "label": "Principal component algorithm",
            "parameters": [
                {
                    "name": "y",
                    "label": "y",
                    "value": "rightppplanumpolare,righthippocampus,lefthippocampus,rightamygdala,leftamygdala"
                },
                {
                    "name": "pathology",
                    "label": "pathology",
                    "value": "dementia:0.1"
                },
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "edsd0,edsd1,edsd8,edsd9"
                },
                {
                    "name": "filter",
                    "label": "filter",
                    "value": ""
                }
            ],
            "type": "mipengine"
        },
        "name": "Pca"
    },
    {
        "algorithm": {
            "name": "pearson",
            "label": "Pearson Correlation",
            "parameters": [
                {
                    "name": "y",
                    "value": "rightsplsuperiorparietallobule,rightttgtransversetemporalgyrus,leftcaudate,leftocpoccipitalpole"
                },
                {
                    "name": "pathology",
                    "value": "dementia:0.1"
                },
                {
                    "name": "dataset",
                    "value": "edsd0,edsd1,edsd8,edsd9"
                },
                {
                    "name": "filter",
                    "value": ""
                },
                {
                    "name": "alpha",
                    "value": "0.9529895484370635"
                }
            ],
            "type": "mipengine"
        },
        "name": "pearson"
    },
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
    algorithm = json.loads(response.text)
    assert not algorithm["shared"]
    assert algorithm["status"] == "pending"
    assert test_input["algorithm"]["name"] == algorithm["algorithm"]["name"]
    assert test_input["algorithm"]["label"] == algorithm["algorithm"]["label"]
    assert test_input["algorithm"]["type"] == algorithm["algorithm"]["type"]
    while True:
        algorithm_curent_state_response = do_get_experiment_request(algorithm["uuid"])
        algorithm_curent_state = json.loads(algorithm_curent_state_response.text)
        status = algorithm_curent_state["status"]
        print(status)
        if status != "pending":
            assert status == "success"
            assert algorithm_curent_state["result"] is not None
            break
        time.sleep(2)
