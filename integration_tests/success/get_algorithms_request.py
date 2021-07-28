import pytest
import json
import requests


def test_get_algorithms_request():
    url = "http://127.0.0.1:8080/services/algorithms"
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    print(f"Algorithms result-> {response.text}")
    algorithms = json.loads(response.text)
    assert len(algorithms) == 32

    mip_engine_algorithms = [algorithm for algorithm in algorithms if algorithm["type"] == "mipengine"]
    logistic_regression = mip_engine_algorithms[0]
    print(f"mip_engine_algorithms-> {mip_engine_algorithms}")
    assert len(mip_engine_algorithms) == 1
    assert logistic_regression["name"] == "LOGISTIC_REGRESSION"

    galaxy_algorithms = [algorithm for algorithm in algorithms if algorithm["type"] == "workflow"]
    print(f"galaxy_algorithms-> {galaxy_algorithms}")
    assert len(galaxy_algorithms) == 2

    exareme_engine_algorithms = [algorithm for algorithm in algorithms if
                                 algorithm["type"] not in ["mipengine", "workflow"]]
    print(f"exareme_engine_algorithms-> {exareme_engine_algorithms}")
    assert len(exareme_engine_algorithms) == 29

