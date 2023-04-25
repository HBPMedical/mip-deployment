# Update of the worker node metadata file

:warning: This readme will only focus on the case where the CDE remained the same and a new dataset has been added to the nodes

## Context

Eachworker nodes inside a federation needs to share the same metadata file.
This file describes the shape of the datasets as well as a list of datasets available to the node.

A example of the file is availabe in this repository [here](https://github.com/HBPMedical/mip-deployment/blob/master/data/dementia/CDEsMetadata.json)

There is two cases in which we need to update the metadata file (both can happen at the same time):
- The CDE has changed meaning that the shape of the datasets is not the same.
- A new dataset is added, and the list of datasets needs to be updated

In Exareme 2 this process is automated, in Exareme 1 the task has to be performed manually / programatically through a script. 

:warning: Up to version 7.1, the MIP relies on Exareme 1. This dependency will be removed in the next release (version 8).

## Upgrading manually


In a worker node, there is as many metadata files as their is federation.

If a new dataset is added to the `dementia` federation then the relevent file will be located under `/data/dementia/CDEsMetadata.json`

Concider this snippet of metadatafile:

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
- the code of the variable is  `dataset`
- the list of datasets is available inside the `enumeration` key

Given a new dataset of `code` demo and `label` demo-dataset, the updated metadata file needs to look as such:

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
