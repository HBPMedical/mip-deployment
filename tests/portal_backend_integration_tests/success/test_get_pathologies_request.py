import pytest
import json
import requests


def test_get_pathologies_request():
    url = "http://172.17.0.1:8080/services/pathologies"
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    print(f"Pathologies result-> {response.text}")
    pathologies = json.loads(response.text)
    assert len(pathologies) == 3
    assert all(pathology["code"] in ["dementia", "mentalhealth", "tbi"] for pathology in pathologies)
    assert all(len(pathology["datasets"]) in [21, 185, 192] for pathology in pathologies)



