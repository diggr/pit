# PIT - Provenance Integration Tools

Author: P. Mühleder <muehleder@ub.uni-leipzig.de>

## Description

Keeping track of provenance information of datasets can be difficult, 
especially in small scale, experimental research environments in the humanities, 
where research data sets were often stored on personal computers without
a clear research data management strategy.

PIT provides a lightweight, flexible tool to assist you to keep track of your 
data provenance without the need of building a dedicated, centralized 
infrastructure. Provenance information is written either directly into
the datafiles (.json files) or in corresponding .prov files. 

It provides a python package for handling dataset import and export,
as well as a command line tool for adding and updating provenance 
information for your data files.

The provenance information can be displayed as a data tree and
exported as an ttl RDF file, using the PROV-O vocabulary 
(https://www.w3.org/TR/prov-o/).

PIT Store Object currently supports the following file types:
* .json
* .csv

Via the command line tool, provenance information can be added to any file.

Database support is planned.

## Main elements

### Provenance object

### Store object

### Pit command line tool


## Installation with setuptools

```
git clone http://www.github.com/missinglinks/pit
cd pit/
pip install .
```

## Usage

### Command line tool

```
pit <filename> <params>
```

Parameters:
* --add: add provenance information
** -o <string>: provenance information - original data source
** -s <file_name>: provenance information - concrete data source
** -d <string>: provenance information - short description of data manipulation process
** -a <string>: provenance information - agent responsible for data manipulation
* --rdf <output_file>: export provenance information to specified file
** --img: generate image file with provenance tree as network


### Python library

```
#load original json file
original = load_json("testdata/abc.json")
#set provenance information
original.set_prov(origin="original data resource", desc="accessed via api", agent="my api script")
#save file with provenance information into new file
original.save_to("testdata/abc_with_prov.json")
```

## Thanks

PIT uses the folloing awesome python packages:
* click - http://click.pocoo.org/5/
* prov[dot] - https://github.com/trungdong/prov