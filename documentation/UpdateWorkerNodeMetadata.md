# Data consolidation of the CDEs Metadata files

:warning: This readme will only focus on the case where the CDEs remained the same but a new dataset has been added to the pathology.

## Context

Each node inside a federation. workers and master, need to have the same metadata file.
This file contains information about the CDEs and about all the available datasets.

A example of the file is availabe in this repository [here](https://github.com/HBPMedical/mip-deployment/blob/master/data/dementia/CDEsMetadata.json)

In the case where one or more datasets are added we need to update the metadata file, across all nodes.

In Exareme 2 this process is automated, in Exareme 1 the task has to be performed manually / programatically through a script. 

:warning: Up to version 7.1, the MIP relies on Exareme 1. This dependency will be removed in the next major release (version 8).

## Updating manually

In a node, there are as many metadata files as there are pathologies, in that node.

If a new dataset is added to the `dementia` pathology then the relevant file will be located under `/data/dementia/CDEsMetadata.json`

Concider this snippet of metadata file:

```json
    {
        "variables": [
            {
                "isCategorical": true,
                "code": "dataset",
                "sql_type": "text",
                "description": "Variable used to differentiate datasets",
                "enumerations": [
                    {
                        "code": "ppmi",
                        "label": "PPMI"
                    },
                    {
                        "code": "edsd",
                        "label": "EDSD"
                    },
                    {
                        "code": "desd-synthdata",
                        "label": "DESD-synthdata"
                    },
                    {
                        "code": "fake_longitudinal",
                        "label": "Longitudinal"
                    }
                ],
                "label": "Dataset",
                "units": "",
                "type": "nominal",
                "methodology": "mip-cde"
            },
    }
```

This block represents the variable where the list of dataset is specified:
- the code of the variable is `dataset`
- the list of datasets is available inside the `enumerations` key

Given a new dataset of code `demo` and label `demo-dataset`, the updated metadata file needs to look as such:

```json
    {
        "variables": [
            {
                "isCategorical": true,
                "code": "dataset",
                "sql_type": "text",
                "description": "Variable used to differentiate datasets",
                "enumerations": [
                    {
                        "code": "ppmi",
                        "label": "PPMI"
                    },
                    {
                        "code": "edsd",
                        "label": "EDSD"
                    },
                    {
                        "code": "desd-synthdata",
                        "label": "DESD-synthdata"
                    },
                    {
                        "code": "fake_longitudinal",
                        "label": "Longitudinal"
                    },
                    {
                        "code": "demo",
                        "label": "demo-dataset"
                    }
                    
                ],
                "label": "Dataset",
                "units": "",
                "type": "nominal",
                "methodology": "mip-cde"
            },
    }
```
