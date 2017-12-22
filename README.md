# PIT - Provenance Integration Tools

Author: P. Mühleder <muehleder@ub.uni-leipzig.de>

## Description

Keeping track of provenance information of datasets can be difficult, 
especially in small scale, experimental research environments. 

PIT provides a lightweight, flexible solution to keep track of your 
data provenance without the need of building a dedicated, centralized 
infrastructure. Provenance information is written either directly into
the datafiles (.json files) or in corresponding .prov files. 

It provides a python package for handling dataset import and export,
as well as a command line tool for adding and updating provenance 
information for your data files.

The provenance information can be displayed as a data tree and
exported as an ttl RDF file, using the PROV-O vocabulary 
(https://www.w3.org/TR/prov-o/).

PIT currently supports the following file types:
* .json
* .csv
* (via the command line tool, provenance information can be added to
any file)

and the following database backends:
* Couch DB


## Installation

## Usage

### Command line tool

### Python library

## Thanks

PIT uses the folloing awesome python packages:
* click - http://click.pocoo.org/5/
* prov[dot] - https://github.com/trungdong/prov