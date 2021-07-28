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
    ("Invalid name",
     {
         "algorithm": {
             "name": "LOGISTIC_REGRES",
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
     }
     ),
    ("Invalid label",
     {
         "algorithm": {
             "name": "LOGISTIC_REGRESSION",
             "label": "Logistic",
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
     }
     ),
    ("Invalid parameter name",
     {
         "algorithm": {
             "name": "LOGISTIC_REGRESSION",
             "label": "Logistic Regression",
             "parameters": [
                 {
                     "name": "xyz",
                     "label": "x",
                     "value": "rightppplanumpolare,righthippocampus,lefthippocampus,rightamygdala,leftamygdala"
                 },
                 {
                     "name": "xyz",
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
     }
     ),
    ("Invalid parameter label",
     {
         "algorithm": {
             "name": "LOGISTIC_REGRESSION",
             "label": "Logistic Regression",
             "parameters": [
                 {
                     "name": "x",
                     "label": "xyz",
                     "value": "rightppplanumpolare,righthippocampus,lefthippocampus,rightamygdala,leftamygdala"
                 },
                 {
                     "name": "y",
                     "label": "xyz",
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
     }
     ),
    ("Invalid parameter value",
     {
         "algorithm": {
             "name": "LOGISTIC_REGRESSION",
             "label": "Logistic Regression",
             "parameters": [
                 {
                     "name": "x",
                     "label": "x",
                     "value": "xyz"
                 },
                 {
                     "name": "y",
                     "label": "y",
                     "value": "xyz"
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
     }
     ),
]


@pytest.mark.parametrize(
    "test_case,test_input", all_success_cases
)
def test_post_request_exareme(test_case, test_input):
    url = "http://127.0.0.1/services/experiments"

    request_json = json.dumps(test_input)

    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(url, data=request_json, headers=headers)

    algorithm = json.loads(response.text)
    assert test_input["algorithm"]["name"] == algorithm["algorithm"]["name"]
    assert test_input["algorithm"]["label"] == algorithm["algorithm"]["label"]
    assert test_input["algorithm"]["type"] == algorithm["algorithm"]["type"]
    while True:
        logistic_current_state_response = do_get_experiment_request(algorithm["uuid"])
        logistic_current_state = json.loads(logistic_current_state_response.text)
        status = logistic_current_state["status"]
        if status != "pending":
            print(test_case)
            print(logistic_current_state["result"])
            assert status == "error"
            assert "result" not in logistic_current_state
            break
        time.sleep(2)


def test_post_request_exareme_invalid_parameter_type():
    url = "http://127.0.0.1/services/experiments"

    request_json = json.dumps(
        {
            "algorithm": {
                "name": "LOGISTIC_REGRESSION",
                "label": "Logistic Regression",
                "parameters": "xyz",
                "type": "python_iterative"
            },
            "name": "LOGISTIC_REGRESSION"
        }
    )

    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(url, data=request_json, headers=headers)
    assert response.text == ""