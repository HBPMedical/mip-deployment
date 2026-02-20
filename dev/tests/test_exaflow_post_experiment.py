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
            "parameters": [
                {"name": "dataset", "value": "dummy_tbi"},
                {"name": "filter", "value": ""},
                {"name": "pathology", "value": "tbi:0.1"},
                {
                    "name": "y",
                    "value": "pupil_reactivity_right_eye_result",
                },
            ],
            "name": "descriptive_stats",
        },
        "name": "Descriptive analysis",
    },
    {
        "algorithm": {
            "name": "pca",
            "parameters": [
                {
                    "name": "y",
                    "value": "rightppplanumpolare,righthippocampus,lefthippocampus,rightamygdala,leftamygdala",
                },
                {"name": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "value": "edsd",
                },
                {"name": "filter", "value": None},
            ],
        },
        "name": "Principal component algorithm",
    },
    {
        "algorithm": {
            "name": "pearson_correlation",
            "parameters": [
                {
                    "name": "y",
                    "value": "rightsplsuperiorparietallobule,rightttgtransversetemporalgyrus,leftcaudate,leftocpoccipitalpole",
                },
                {"name": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "value": "edsd",
                },
                {"name": "filter", "value": ""},
                {"name": "alpha", "value": "0.9529895484370635"},
            ],
        },
        "name": "Pearson Correlation",
    },
    {
        "algorithm": {
            "name": "anova_oneway",
            "parameters": [
                {"name": "y", "value": "leftententorhinalarea"},
                {"name": "x", "value": "neurodegenerativescategories"},
                {"name": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "value": "desd-synthdata,ppmi",
                },
                {
                    "name": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": true}',
                },
            ],
        },
        "name": "One Way Anova",
    },
    {
        "algorithm": {
            "name": "linear_regression",
            "parameters": [
                {"name": "y", "value": "rightcuncuneus"},
                {
                    "name": "x",
                    "value": "rightioginferioroccipitalgyrus,leftententorhinalarea,rightamygdala,leftmpogpostcentralgyrusmedialsegment,rightporgposteriororbitalgyrus,leftpoparietaloperculum,righttrifgtriangularpartoftheinferiorfrontalgyrus,rightmpogpostcentralgyrusmedialsegment,rightlateralventricle,rightmfcmedialfrontalcortex,rightorifgorbitalpartoftheinferiorfrontalgyrus,opticchiasm,neurodegenerativescategories,rightpcggposteriorcingulategyrus",
                },
                {"name": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "value": "desd-synthdata,ppmi,edsd",
                },
                {
                    "name": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi", "edsd"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "rightcuncuneus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightioginferioroccipitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightamygdala", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightporgposteriororbitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftpoparietaloperculum", "type": "string", "operator": "is_not_null", "value": null}, {"id": "righttrifgtriangularpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightlateralventricle", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmfcmedialfrontalcortex", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightorifgorbitalpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "opticchiasm", "type": "string", "operator": "is_not_null", "value": null}, {"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightpcggposteriorcingulategyrus", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": True}',
                },
            ],
        },
        "name": "Linear Regression",
    },
    {
        "algorithm": {
            "name": "linear_regression_cv",
            "parameters": [
                {"name": "y", "value": "leftocpoccipitalpole"},
                {
                    "name": "x",
                    "value": "righthippocampus,rightsogsuperioroccipitalgyrus,leftppplanumpolare,leftsmgsupramarginalgyrus,leftgregyrusrectus,rightitginferiortemporalgyrus,leftcalccalcarinecortex",
                },
                {"name": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "value": "desd-synthdata,ppmi,edsd",
                },
                {
                    "name": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi", "edsd"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "rightcuncuneus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightioginferioroccipitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightamygdala", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightporgposteriororbitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftpoparietaloperculum", "type": "string", "operator": "is_not_null", "value": null}, {"id": "righttrifgtriangularpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightlateralventricle", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmfcmedialfrontalcortex", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightorifgorbitalpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "opticchiasm", "type": "string", "operator": "is_not_null", "value": null}, {"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightpcggposteriorcingulategyrus", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": True}',
                },
                {
                    "name": "n_splits",
                    "label": "n_splits",
                    "value": 4,
                },
            ],
        },
        "name": "Linear Regression CV",
    },
    {
        "algorithm": {
            "name": "linear_regression_cv",
            "parameters": [
                {"name": "y", "value": "righthippocampus"},
                {
                    "name": "x",
                    "value": "lefthippocampus",
                },
                {
                    "name": "pathology",
                    "value": "dementia_longitudinal:v1",
                },
                {
                    "name": "dataset",
                    "value": "desd-synthdata",
                },
                {
                    "name": "filter",
                    "value": "",
                },
                {
                    "name": "n_splits",
                    "value": 4,
                },
            ],
            "preprocessing": [
                {
                    "name": "longitudinal_transformer",
                    "parameters": [
                        {
                            "name": "visit1",
                            "value": "BL",
                        },
                        {
                            "name": "visit2",
                            "value": "FL1",
                        },
                        {
                            "name": "strategies",
                            "value": '{"righthippocampus": "first", "lefthippocampus": "diff"}',
                        },
                    ],
                }
            ],
        },
        "name": "Linear Regression CV Longitudinal",
    },
    {
        "algorithm": {
            "name": "ttest_independent",
            "parameters": [
                {"name": "y", "value": "rightgregyrusrectus"},
                {
                    "name": "x",
                    "value": "dataset",
                },
                {"name": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "value": "desd-synthdata,ppmi,edsd",
                },
                {
                    "name": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi", "edsd"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "rightcuncuneus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightioginferioroccipitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightamygdala", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightporgposteriororbitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftpoparietaloperculum", "type": "string", "operator": "is_not_null", "value": null}, {"id": "righttrifgtriangularpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightlateralventricle", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmfcmedialfrontalcortex", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightorifgorbitalpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "opticchiasm", "type": "string", "operator": "is_not_null", "value": null}, {"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightpcggposteriorcingulategyrus", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": True}',
                },
                {
                    "name": "alt_hypothesis",
                    "value": "less",
                },
                {
                    "name": "alpha",
                    "value": 0.5727207100545569,
                },
                {
                    "name": "groupA",
                    "value": "edsd",
                },
                {
                    "name": "groupB",
                    "value": "ppmi",
                },
            ],
        },
        "name": "T-Test Independent",
    },
    {
        "algorithm": {
            "name": "logistic_regression",
            "parameters": [
                {"name": "y", "value": "alzheimerbroadcategory"},
                {
                    "name": "x",
                    "value": "rightttgtransversetemporalgyrus,leftpinsposteriorinsula,leftpoparietaloperculum,rightptplanumtemporale,leftventraldc",
                },
                {"name": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "value": "desd-synthdata,ppmi",
                },
                {
                    "name": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi", "edsd"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "rightcuncuneus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightioginferioroccipitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightamygdala", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightporgposteriororbitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftpoparietaloperculum", "type": "string", "operator": "is_not_null", "value": null}, {"id": "righttrifgtriangularpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightlateralventricle", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmfcmedialfrontalcortex", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightorifgorbitalpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "opticchiasm", "type": "string", "operator": "is_not_null", "value": null}, {"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightpcggposteriorcingulategyrus", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": True}',
                },
                {
                    "name": "positive_class",
                    "value": "Other",
                },
            ],
        },
        "name": "Logistic Regression",
    },
    {
        "algorithm": {
            "name": "logistic_regression_cv",
            "parameters": [
                {"name": "y", "value": "alzheimerbroadcategory"},
                {
                    "name": "x",
                    "value": "leftopifgopercularpartoftheinferiorfrontalgyrus,rightmsfgsuperiorfrontalgyrusmedialsegment,leftbasalforebrain,leftinflatvent",
                },
                {"name": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "value": "desd-synthdata,ppmi,edsd",
                },
                {
                    "name": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi", "edsd"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "rightcuncuneus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightioginferioroccipitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightamygdala", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightporgposteriororbitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftpoparietaloperculum", "type": "string", "operator": "is_not_null", "value": null}, {"id": "righttrifgtriangularpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightlateralventricle", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmfcmedialfrontalcortex", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightorifgorbitalpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "opticchiasm", "type": "string", "operator": "is_not_null", "value": null}, {"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightpcggposteriorcingulategyrus", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": True}',
                },
                {
                    "name": "positive_class",
                    "value": "AD",
                },
                {
                    "name": "n_splits",
                    "value": 3,
                },
            ],
        },
        "name": "Logistic Regression CV",
    },
    {
        "algorithm": {
            "name": "ttest_paired",
            "parameters": [
                {"name": "y", "value": "rightppplanumpolare"},
                {
                    "name": "x",
                    "value": "rightorifgorbitalpartoftheinferiorfrontalgyrus",
                },
                {"name": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "value": "desd-synthdata,ppmi,edsd",
                },
                {
                    "name": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi", "edsd"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "rightcuncuneus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightioginferioroccipitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightamygdala", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightporgposteriororbitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftpoparietaloperculum", "type": "string", "operator": "is_not_null", "value": null}, {"id": "righttrifgtriangularpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightlateralventricle", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmfcmedialfrontalcortex", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightorifgorbitalpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "opticchiasm", "type": "string", "operator": "is_not_null", "value": null}, {"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightpcggposteriorcingulategyrus", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": True}',
                },
                {
                    "name": "alt_hypothesis",
                    "value": "less",
                },
                {
                    "name": "alpha",
                    "value": 0.06109997172168302,
                },
            ],
        },
        "name": "Paired t-test",
    },
    {
        "algorithm": {
            "name": "ttest_onesample",
            "parameters": [
                {"name": "y", "value": "leftmcggmiddlecingulategyrus"},
                {
                    "name": "x",
                    "value": "rightorifgorbitalpartoftheinferiorfrontalgyrus",
                },
                {"name": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "value": "desd-synthdata,edsd",
                },
                {
                    "name": "filter",
                    "value": '{"condition": "AND", "rules": [{"id": "dataset", "type": "string", "value": ["desd-synthdata", "ppmi", "edsd"], "operator": "in"}, {"condition": "AND", "rules": [{"id": "rightcuncuneus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightioginferioroccipitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftententorhinalarea", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightamygdala", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightporgposteriororbitalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "leftpoparietaloperculum", "type": "string", "operator": "is_not_null", "value": null}, {"id": "righttrifgtriangularpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmpogpostcentralgyrusmedialsegment", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightlateralventricle", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightmfcmedialfrontalcortex", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightorifgorbitalpartoftheinferiorfrontalgyrus", "type": "string", "operator": "is_not_null", "value": null}, {"id": "opticchiasm", "type": "string", "operator": "is_not_null", "value": null}, {"id": "neurodegenerativescategories", "type": "string", "operator": "is_not_null", "value": null}, {"id": "rightpcggposteriorcingulategyrus", "type": "string", "operator": "is_not_null", "value": null}]}], "valid": True}',
                },
                {
                    "name": "alt_hypothesis",
                    "value": "greater",
                },
                {
                    "name": "alpha",
                    "value": 0.6764545707122654,
                },
                {
                    "name": "mu",
                    "value": -1.7510563394418988,
                },
            ],
        },
        "name": "T-Test One-Sample",
    },
    {
        "algorithm": {
            "name": "descriptive_stats",
            "parameters": [
                {
                    "name": "y",
                    "value": "leftttgtransversetemporalgyrus,rightmprgprecentralgyrusmedialsegment",
                },
                {"name": "pathology", "value": "dementia:0.1"},
                {
                    "name": "dataset",
                    "value": "desd-synthdata,edsd,ppmi",
                },
                {
                    "name": "filter",
                    "value": "",
                },
            ],
        },
        "name": "Descriptive stats",
    },
]


@pytest.mark.parametrize("test_input", all_success_cases)
def test_post_request_exaflow(test_input):

    url = "http://127.0.0.1:8080/services/experiments"

    print(f"POST to {url}")
    request_json = json.dumps(test_input)

    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.post(url, data=request_json, headers=headers)

    print(f"POST Exaflow result-> {response.text}")
    algorithm = json.loads(response.text)
    assert not algorithm["shared"]
    assert algorithm["status"] == "pending"
    assert test_input["algorithm"]["name"] == algorithm["algorithm"]["name"]
    while True:
        algorithm_current_state_response = do_get_experiment_request(algorithm["uuid"])
        algorithm_current_state = json.loads(algorithm_current_state_response.text)
        status = algorithm_current_state["status"]
        print(status)
        if status != "pending":
            assert status == "success", f"Result: {algorithm_current_state}"
            assert algorithm_current_state["result"] is not None
            break
        time.sleep(2)
