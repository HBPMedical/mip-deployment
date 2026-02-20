# Data Requirements

This document describes the specifications that any new data (CSVs) **must** have in order to be imported properly.


## CDEsMetadata Requirements:

The CDEsMetadata (Common Data Elements Metadata) is a json file that is used to define the type of the variables inside each csv files.

The metadata file **must** follow these rules:
* It **must** follow a tree structure. The `variables` lists are the leafs and the `groups` lists are the branches where one or more `variables` lists can exist.
* A `variable` inside the `variables` list **must** have these fields:
  * **code** (Variable name)
  * **isCategorical** (true/false)
  * **sql_type** (TEXT, REAL, INT)
  * **type** (nominal, real, integer, text)
* It can also contain:
  * **min** (Integer)
  * **max** (Integer)
  * **enumerations** (List of codes)
* The `dataset` CDE is required.
* In the parent dictionary there will be a `version` property, of string format.

An example can be seen at [CDEs Medatadata](../data/dementia/CDEsMetadata.json).

After adding the CDEsMetadata file you can add your data the same way as adding **New Data on existing Pathology**.

### Longitudinal CDEsMetadata Requirements:

The metadata for the longitudinal analysis pathologies, in addition to the previous, will have the following constraints:
* A pathology will be marked as `longitudinal` with a property in the metadata, similar to the `version`.
* The `subjectID` CDE will be required.
* The `visitID` CDE will be required.
* The `visitID` will be categorical, with enumerations `BL`, `FL1`, `FL2` …

**Important:** The `subjectID` and `visitID` columns must always exist and be filled, in the csvs.


## CSV File Requirements:

A csv file **must** follow these rules:
* The csv file **must** contain at least one row with the variable names (CDEs), like a header, corresponding to the rest of the rows.
* All the column names that exist in the csvs **must** also exist in the CDEsMetadata.json file. The csv can have less columns than the CDEs in the metadata but **NOT** more.
* The `dataset` CDE is **required** to exist in the CDEsMetadata.json and as a column in the csvs.

## New Pathology

If you want to add a new pathology on MIP then you need to create a new folder inside the `data` directory with the name of your pathology. Inside that folder you need to add:
* The CDEsMetadata.json file
* and the CSVs containing the data.