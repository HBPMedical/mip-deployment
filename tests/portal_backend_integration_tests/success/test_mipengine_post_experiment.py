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
            "name": "PCA",
            "label": "Principal component algorithm",
            "parameters": [
                {
                    "name": "y",
                    "label": "y",
                    "value": "rightppplanumpolare,righthippocampus,lefthippocampus,rightamygdala,leftamygdala",
                },
                {"name": "pathology", "label": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "edsd",
                },
                {"name": "filter", "label": "filter", "value": None},
            ],
            "type": "mipengine",
        },
        "name": "Principal component algorithm",
    },
    {
        "algorithm": {
            "name": "pearson_correlation",
            "label": "Pearson Correlation",
            "parameters": [
                {
                    "name": "y",
                    "label": "y",
                    "value": "rightsplsuperiorparietallobule,rightttgtransversetemporalgyrus,leftcaudate,leftocpoccipitalpole",
                },
                {"name": "pathology", "label": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "edsd",
                },
                {"name": "filter", "label": "filter", "value": ""},
                {"name": "alpha", "label": "alpha", "value": "0.9529895484370635"},
            ],
            "type": "mipengine",
        },
        "name": "Pearson Correlation",
    },
    {
        "algorithm": {
            "name": "anova_oneway",
            "label": "One Way Anova",
            "parameters": [
                {"name": "y", "label": "y", "value": "leftententorhinalarea"},
                {"name": "x", "label": "x", "value": "neurodegenerativescategories"},
                {"name": "pathology", "label": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "desd-synthdata,ppmi",
                },
                {
                    "name": "filter",
                    "label": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": true}',
                },
            ],
            "type": "mipengine",
        },
        "name": "One Way Anova",
    },
    {
        "algorithm": {
            "name": "linear_regression",
            "label": "Linear Regression",
            "parameters": [
                {"name": "y", "label": "y", "value": "rightcuncuneus"},
                {
                    "name": "x",
                    "label": "x",
                    "value": "rightioginferioroccipitalgyrus,leftententorhinalarea,rightamygdala,leftmpogpostcentralgyrusmedialsegment,rightporgposteriororbitalgyrus,leftpoparietaloperculum,righttrifgtriangularpartoftheinferiorfrontalgyrus,rightmpogpostcentralgyrusmedialsegment,rightlateralventricle,rightmfcmedialfrontalcortex,rightorifgorbitalpartoftheinferiorfrontalgyrus,opticchiasm,neurodegenerativescategories,rightpcggposteriorcingulategyrus",
                },
                {"name": "pathology", "label": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "desd-synthdata,ppmi,edsd",
                },
                {
                    "name": "filter",
                    "label": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi", "edsd"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "rightcuncuneus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightioginferioroccipitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightamygdala", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightporgposteriororbitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftpoparietaloperculum", "type": "string", "operator": "is_not_null", "value": null}, {"id": "righttrifgtriangularpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightlateralventricle", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmfcmedialfrontalcortex", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightorifgorbitalpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "opticchiasm", "type": "string", "operator": "is_not_null", "value": null}, {"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightpcggposteriorcingulategyrus", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": True}',
                },
            ],
            "type": "mipengine",
        },
        "name": "Linear Regression",
    },
    {
        "algorithm": {
            "name": "linear_regression_cv",
            "label": "Linear Regression CV",
            "parameters": [
                {"name": "y", "label": "y", "value": "leftocpoccipitalpole"},
                {
                    "name": "x",
                    "label": "x",
                    "value": "righthippocampus,rightsogsuperioroccipitalgyrus,leftppplanumpolare,leftsmgsupramarginalgyrus,leftgregyrusrectus,rightitginferiortemporalgyrus,leftcalccalcarinecortex",
                },
                {"name": "pathology", "label": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "desd-synthdata,ppmi,edsd",
                },
                {
                    "name": "filter",
                    "label": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi", "edsd"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "rightcuncuneus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightioginferioroccipitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightamygdala", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightporgposteriororbitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftpoparietaloperculum", "type": "string", "operator": "is_not_null", "value": null}, {"id": "righttrifgtriangularpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightlateralventricle", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmfcmedialfrontalcortex", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightorifgorbitalpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "opticchiasm", "type": "string", "operator": "is_not_null", "value": null}, {"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightpcggposteriorcingulategyrus", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": True}',
                },
                {
                    "name": "n_splits",
                    "label": "n_splits",
                    "value": 4,
                },
            ],
            "type": "mipengine",
        },
        "name": "Linear Regression CV",
    },
    {
        "algorithm": {
            "name": "ttest_independent",
            "label": "T-Test Independent",
            "parameters": [
                {"name": "y", "label": "y", "value": "rightgregyrusrectus"},
                {
                    "name": "x",
                    "label": "x",
                    "value": "rightcuncuneus",
                },
                {"name": "pathology", "label": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "desd-synthdata,ppmi,edsd",
                },
                {
                    "name": "filter",
                    "label": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi", "edsd"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "rightcuncuneus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightioginferioroccipitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightamygdala", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightporgposteriororbitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftpoparietaloperculum", "type": "string", "operator": "is_not_null", "value": null}, {"id": "righttrifgtriangularpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightlateralventricle", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmfcmedialfrontalcortex", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightorifgorbitalpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "opticchiasm", "type": "string", "operator": "is_not_null", "value": null}, {"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightpcggposteriorcingulategyrus", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": True}',
                },
                {
                    "name": "alt_hypothesis",
                    "label": "alt_hypothesis",
                    "value": "less",
                },
                {
                    "name": "confidence_lvl",
                    "label": "confidence_lvl",
                    "value": 0.5727207100545569,
                },
            ],
            "type": "mipengine",
        },
        "name": "T-Test Independent",
    },
    {
        "algorithm": {
            "name": "logistic_regression",
            "label": "Logistic Regression",
            "parameters": [
                {"name": "y", "label": "y", "value": "alzheimerbroadcategory"},
                {
                    "name": "x",
                    "label": "x",
                    "value": "rightttgtransversetemporalgyrus,leftpinsposteriorinsula,leftpoparietaloperculum,rightptplanumtemporale,leftventraldc",
                },
                {"name": "pathology", "label": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "desd-synthdata,ppmi",
                },
                {
                    "name": "filter",
                    "label": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi", "edsd"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "rightcuncuneus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightioginferioroccipitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightamygdala", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightporgposteriororbitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftpoparietaloperculum", "type": "string", "operator": "is_not_null", "value": null}, {"id": "righttrifgtriangularpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightlateralventricle", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmfcmedialfrontalcortex", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightorifgorbitalpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "opticchiasm", "type": "string", "operator": "is_not_null", "value": null}, {"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightpcggposteriorcingulategyrus", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": True}',
                },
                {
                    "name": "positive_class",
                    "label": "positive_class",
                    "value": 'Other',
                },
            ],
            "type": "mipengine",
        },
        "name": "Logistic Regression",
    },
    {
        "algorithm": {
            "name": "logistic_regression_cv",
            "label": "Logistic Regression CV",
            "parameters": [
                {"name": "y", "label": "y", "value": "alzheimerbroadcategory"},
                {
                    "name": "x",
                    "label": "x",
                    "value": "leftopifgopercularpartoftheinferiorfrontalgyrus,rightmsfgsuperiorfrontalgyrusmedialsegment,leftbasalforebrain,leftinflatvent",
                },
                {"name": "pathology", "label": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "desd-synthdata,ppmi,edsd",
                },
                {
                    "name": "filter",
                    "label": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi", "edsd"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "rightcuncuneus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightioginferioroccipitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightamygdala", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightporgposteriororbitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftpoparietaloperculum", "type": "string", "operator": "is_not_null", "value": null}, {"id": "righttrifgtriangularpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightlateralventricle", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmfcmedialfrontalcortex", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightorifgorbitalpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "opticchiasm", "type": "string", "operator": "is_not_null", "value": null}, {"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightpcggposteriorcingulategyrus", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": True}',
                },
                {
                    "name": "positive_class",
                    "label": "positive_class",
                    "value": 'AD',
                },
                {
                    "name": "n_splits",
                    "label": "n_splits",
                    "value": 3,
                },
            ],
            "type": "mipengine",
        },
        "name": "Logistic Regression CV",
    },
    {
        "algorithm": {
            "name": "ttest_paired",
            "label": "Paired t-test",
            "parameters": [
                {"name": "y", "label": "y", "value": "rightppplanumpolare"},
                {
                    "name": "x",
                    "label": "x",
                    "value": "rightorifgorbitalpartoftheinferiorfrontalgyrus",
                },
                {"name": "pathology", "label": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "desd-synthdata,ppmi,edsd",
                },
                {
                    "name": "filter",
                    "label": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi", "edsd"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "rightcuncuneus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightioginferioroccipitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightamygdala", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightporgposteriororbitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftpoparietaloperculum", "type": "string", "operator": "is_not_null", "value": null}, {"id": "righttrifgtriangularpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightlateralventricle", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmfcmedialfrontalcortex", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightorifgorbitalpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "opticchiasm", "type": "string", "operator": "is_not_null", "value": null}, {"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightpcggposteriorcingulategyrus", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": True}',
                },
                {
                    "name": "alt_hypothesis",
                    "label": "alt_hypothesis",
                    "value": 'less',
                },
                {
                    "name": "alpha",
                    "label": "alpha",
                    "value": 0.06109997172168302,
                },
            ],
            "type": "mipengine",
        },
        "name": "Paired t-test",
    },
    {
        "algorithm": {
            "name": "ttest_onesample",
            "label": "T-Test One-Sample",
            "parameters": [
                {"name": "y", "label": "y", "value": "leftmcggmiddlecingulategyrus"},
                {
                    "name": "x",
                    "label": "x",
                    "value": "rightorifgorbitalpartoftheinferiorfrontalgyrus",
                },
                {"name": "pathology", "label": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "label": "dataset",
                    "value": "desd-synthdata,edsd",
                },
                {
                    "name": "filter",
                    "label": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi", "edsd"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "rightcuncuneus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightioginferioroccipitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightamygdala", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightporgposteriororbitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftpoparietaloperculum", "type": "string", "operator": "is_not_null", "value": null}, {"id": "righttrifgtriangularpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightlateralventricle", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmfcmedialfrontalcortex", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightorifgorbitalpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "opticchiasm", "type": "string", "operator": "is_not_null", "value": null}, {"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightpcggposteriorcingulategyrus", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": True}',
                },
                {
                    "name": "alt_hypothesis",
                    "label": "alt_hypothesis",
                    "value": 'greater',
                },
                {
                    "name": "alpha",
                    "label": "alpha",
                    "value": 0.6764545707122654,
                },
                {
                    "name": "mu",
                    "label": "mu",
                    "value": -1.7510563394418988,
                },
            ],
            "type": "mipengine",
        },
        "name": "T-Test One-Sample",
    },
]


@pytest.mark.parametrize("test_input", all_success_cases)
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
