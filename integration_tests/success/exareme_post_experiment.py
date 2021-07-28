import json
import time

import pytest
import requests


def do_get_experiment_request(uuid):
    url = f"http://127.0.0.1/services/experiments/{uuid}"
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
                    "name": "formula",
                    "label": "formula",
                    "value": ""
                },
                {
                    "name": "positive_level",
                    "label": "Positive level",
                    "value": "AD"
                },
                {
                    "name": "negative_level",
                    "label": "Negative level",
                    "value": "CN"
                }
            ],
            "type": "python_iterative"
        },
        "name": "dsafas"
    },
    {
       "algorithm":{
          "name":"NAIVE_BAYES",
          "label":"Naive Bayes classifier",
          "parameters":[
             {
                "name":"x",
                "label":"x",
                "value":"righthippocampus,lefthippocampus"
             },
             {
                "name":"y",
                "label":"y",
                "value":"alzheimerbroadcategory"
             },
             {
                "name":"alpha",
                "label":"alpha",
                "value":"0.1"
             },
             {
                "name":"k",
                "label":"number of batches",
                "value":"10"
             },
             {
                "name":"pathology",
                "label":"pathology",
                "value":"dementia"
             },
             {
                "name":"dataset",
                "label":"dataset",
                "value":"edsd"
             },
             {
                "name":"filter",
                "label":"filter",
                "value":""
             }
          ],
          "type":"python_multiple_local_global"
       },
       "name":"Naive Bayes classifier"
    },
    {
       "algorithm":{
          "name":"TTEST_PAIRED",
          "label":"T-Test Paired",
          "parameters":[
             {
                "name":"y",
                "label":"y",
                "value":"righthippocampus-lefthippocampus"
             },
             {
                "name":"hypothesis",
                "label":"hypothesis",
                "value":"different"
             },
             {
                "name":"pathology",
                "label":"pathology",
                "value":"dementia"
             },
             {
                "name":"dataset",
                "label":"dataset",
                "value":"desd-synthdata"
             },
             {
                "name":"filter",
                "label":"filter",
                "value":""
             }
          ],
          "type":"local_global"
       },
       "name":"T-Test Paired"
    }
]


@pytest.mark.parametrize(
    "test_input", all_success_cases
)
def test_post_request_exareme(test_input):
    url = "http://127.0.0.1/services/experiments"

    print(f"POST to {url}")
    request_json = json.dumps(test_input)

    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(url, data=request_json, headers=headers)
    algorithm = json.loads(response.text)
    assert test_input["algorithm"]["name"] == algorithm["algorithm"]["name"]
    assert test_input["algorithm"]["label"] == algorithm["algorithm"]["label"]
    assert test_input["algorithm"]["type"] == algorithm["algorithm"]["type"]
    while True:
        logistic_curent_state_response = do_get_experiment_request(algorithm["uuid"])
        logistic_curent_state = json.loads(logistic_curent_state_response.text)
        status = logistic_curent_state["status"]
        print(status)
        if status != "pending":
            assert status == "success"
            assert logistic_curent_state["result"] is not None
            assert algorithm["algorithm"]["type"] != "mipengine"
            assert algorithm["algorithm"]["type"] != "workflow"
            break
        time.sleep(2)

    print(f"POST Exareme result-> {algorithm}")
