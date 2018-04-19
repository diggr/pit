# P(ROV)IT - PROVenance integration tools

![Python 3.6](https://img.shields.io/badge/Python-3.6-blue.svg)
[![GitHub license](https://img.shields.io/github/license/diggr/pit.svg)](https://github.com/diggr/pit/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/diggr/pit.svg)](https://github.com/diggr/pit/issues)

PIT is a light, dezentralized provenance tracking framework. 
It allows the user to track workflows and modifications of
data and files. A subset of the [W3C](https://www.w3.org/) [PROV-O vocabulary](https://www.w3.org/TR/prov-o/) is implemented.

## Requirements

This Software was tested with Python 3.6

## Installation

Installation via [pip](https://pypi.org/) is recommended for end users. We strongly encourage end users
 to make use of a [virtualenv](https://virtualenv.pypa.io/en/stable/). 

### pip

Clone the repository and create a virtualenv.

```zsh
git clone https://github.com/diggr/pit
mkvirtualenv provit
```

Install it with pip

```zsh
pip install PATH_TO_PIT_REPOSITORY 
```

### git / Development

Clone the repository and create a virtualenv.

```zsh
git clone https://github.com/diggr/pit
mkvirtualenv provit
```

Install it with pip in *editable* mode

```zsh
pip install -e PATH_TO_PIT_REPOSITORY 
```


## Usage

Provenance Integration Tools provide a command line client which can be used *out of the box* 
to enrich any file based data with provenance information. Furthermore the provenance class
and vocabulary shipped with *PIT* can be used within other applications.

### Command Line Client

Usage: 

```zsh
pit [OPTIONS] FILEPATH
```

Options:
* **--add**:               Add provenance information layer to file
* **-a, --agent TEXT**:    Provenance information: agent
* **--activity TEXT**:     Provenane information: activity
* **-d, --desc TEXT**:     Provenance information: Description of the data manipulation process
* **-o, --origin TEXT**:   Provenance information: Data origin
* **-s, --sources TEXT**:  Provenance information: Source files
* **--help**:              Show this message and exit.

### Provenance Class

```python
from pit.prov import Provenance

# load prov data for a file, or create new prov for file
prov = Provenance(<filepath>)

# add provenance metadata
prov.add(agent="agent", activity="activity", description="...")
prov.add_primary_source("primary_source", url="http://...", comment="...")
prov.add_sources(["filepath1", "filepath2"])

# return provenance as json tree
prov_dict = prov.tree()

# save provenance metadata into "<filename>.prov" file
prov.save()
```

## License

MIT

## Copyright

* 2018, P. Mühleder
* 2018, [Universitätsbibliothek Leipzig](https://ub.uni-leipzig.de)

## Authors

* P. Mühleder <muehleder@ub.uni-leipzig.de>
* F. Rämisch <raemisch@ub.uni-leipzig.de>