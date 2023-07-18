import pytest
import json
import requests


def test_get_algorithms_request():
    url = "http://172.17.0.1:8080/services/algorithms"
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    print(f"Algorithms result-> {response.text}")
    algorithms = json.loads(response.text)
    # assert len(algorithms) == 34

    EXAREME2_algorithms = [
        algorithm for algorithm in algorithms if algorithm["type"] == "exareme2"
    ]

    assert len(EXAREME2_algorithms) == 16

    exareme_engine_algorithms = [
        algorithm
        for algorithm in algorithms
        if algorithm["type"] not in ["exareme2", "workflow"]
    ]
    print(f"exareme_engine_algorithms-> {exareme_engine_algorithms}")
    assert len(exareme_engine_algorithms) == 16
