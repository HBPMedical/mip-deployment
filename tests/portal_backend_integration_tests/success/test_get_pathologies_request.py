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

    assert all(
        pathology["code"] in ["dementia", "mentalhealth", "tbi"]
        for pathology in pathologies
    )

    assert all(
        len(pathology["datasets"]) in [1, 4, 1] for pathology in pathologies
    )

    assert all(
        count_datasets_from_cdes(pathology["metadataHierarchy"]) in [1, 4, 1] for pathology in pathologies
    )

    assert all(
        count_cdes(pathology["metadataHierarchy"]) in [20, 185, 191] for pathology in pathologies
    )


def count_cdes(metadata_hierarchy) -> int:
    counter = 0

    if "variables" in metadata_hierarchy:
        counter += len(metadata_hierarchy["variables"])

    if "groups" in metadata_hierarchy:
        for cde in metadata_hierarchy["groups"]:
            counter += count_cdes(cde)
    return counter


def count_datasets_from_cdes(metadata_hierarchy) -> int:
    if "variables" in metadata_hierarchy:
        for variable in metadata_hierarchy["variables"]:
            if variable["code"] == "dataset":
                return len(variable["enumerations"])

    if "groups" in metadata_hierarchy:
        for cde in metadata_hierarchy["groups"]:
            counter = count_datasets_from_cdes(cde)
            if counter != 0:
                return counter
    return 0
