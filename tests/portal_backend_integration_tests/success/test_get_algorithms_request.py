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
    assert len(algorithms) == 31

    mip_engine_algorithms = [algorithm for algorithm in algorithms if algorithm["type"] == "mipengine"]
    print(f"mip_engine_algorithms-> {mip_engine_algorithms}")
    assert len(mip_engine_algorithms) == 2

    exareme_engine_algorithms = [algorithm for algorithm in algorithms if
                                 algorithm["type"] not in ["mipengine", "workflow"]]
    print(f"exareme_engine_algorithms-> {exareme_engine_algorithms}")
    assert len(exareme_engine_algorithms) == 29
