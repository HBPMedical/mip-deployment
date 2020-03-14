# New Data Requirements

This document describes the specifications that any new data (CSVs) should have in order to be imported properly.

# New Data on existing Pathology

If you don't want to create a new pathology with <b>custom variables</b> then you just need to add your data, in csv format, inside the pathology folder in the `data` directory, for example in the `data/dementia` directory.

There can be many csv files in a pathology. A csv file should follow these rules:
<ul><li>The csv file should contain at least one row with the variable names (CDEs), like a header, corresponding to the rest of the rows.</li>
	<li>It should contain a subjectcode variable, with the pseudo-id of each record,</li>
	<li>and the dataset column, that declares in which dataset the row belongs to.</li>
	<li>All the variable names should exist in the CDEsMetadata.json file, except from the <code>subjectcode</code>.</li>
</ul>

If your data do not match the specifications of MIP, a message will be shown when installing the software.

# New Pathology

If you want to add a new pathology on MIP then you need to create a new folder inside the `data` directory with the name of your pathology. Inside that folder you need to add:
<ul><li>The CDEsMetadata.json file</li>
	<li>and the CSVs containing the data.</li>
</ul>

## CDEsMetadata:

The CDEsMetadata (Common Data Elements Metadata) is a json file that is used to define the type of the variables inside each csv files.

The metadata file should follow these rules:
<ul>
	<li>It should follow a tree structure. The <code>variables</code> lists are the leafs and the <code>groups</code> lists are the branches where one or more <code>variables</code> lists can exist.</li>
	<li>A <code>variable</code> inside the <code>variables</code> list must have these fields:
		<ul>
			<li><b>code</b> (Variable name)</li>
			<li><b>isCategorical</b> (true/false)</li>
			<li><b>sql_type</b> (TEXT, REAL, INT)</li>
		</ul>
	</li>
	<li>It can also contain:
		<ul>
			<li><b>min</b> (Integer)</li>
			<li><b>max</b> (Integer)</li>
			<li><b>enumerations</b> (List of codes)</li>
		</ul>
	</li>
</ul>

An example can be seen <a href="../data/dementia/CDEsMetadata.json">here</a>.

After adding the CDEsMetadata file you can add your data the same way as adding <b>New Data on existing Pathology</b>.