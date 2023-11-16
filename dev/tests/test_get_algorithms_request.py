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
    assert len(algorithms) == 19
