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
$ git clone https://github.com/diggr/pit
$ mkvirtualenv provit
```

Install it with pip

```zsh
$ pip install PATH_TO_PIT_REPOSITORY 
```

### git / Development

Clone the repository and create a virtualenv.

```zsh
$ git clone https://github.com/diggr/pit
$ mkvirtualenv provit
```

Install it with pip in *editable* mode

```zsh
$ pip install -e PATH_TO_PIT_REPOSITORY 
```


## Usage

Provenance Integration Tools provide a command line client which can be used *out of the box* 
to enrich any file based data with provenance information. Furthermore the provenance class
and vocabulary shipped with *PIT* can be used within other applications.

### Command Line Client

Usage: 

```zsh
$ pit [OPTIONS] FILEPATH
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

## Roadmap

General Roadmap containing features we'd like to realize in the project

1. Test Coverage 
2. Browser-GUI
3. Add Persons to Agent, to allow more granular activity tracking

### Feature Wishlist

A more detailed list of specific (smaller) features and functionality.

#### Browser GUI to visualize Provenance Tree

The browser based GUI should visualize the provenance as a graph, maybe using
d3.js. 

#### Notify user if source referenced file changes

Provenance files contain the version of a file if referenced, if an older version
(i.e. not the current version) of a file is referenced, a warning should 
be displayed.

#### File Browser

A file browser showing e.g. all files with missing provenance.

#### Reference Clustering

Inspect files in your *research* folder, and display all references, 
to identify clusters. This could help structuring a messy research directory
without breaking scripts, or at least knowing, which scripts possibly need
to be updated.

## FAQ / Paradigms

### Can I add multiple agents to an activity?

No. The reason is: If you can distinguish the activities or impact of 
the agent, then you have multiple agents with *multiple activities*. E.g.
if you let three students help you proofreading a file and you get
back *1* revised version, then the three students are *1 agent*
as you cannot distinguish between their results. If you get back *3
versions* you have *3 agents* and *3 activities*.


## License

MIT

## Copyright

* 2018, P. Mühleder
* 2018, [Universitätsbibliothek Leipzig](https://ub.uni-leipzig.de)

## Authors

* P. Mühleder <muehleder@ub.uni-leipzig.de>
* F. Rämisch <raemisch@ub.uni-leipzig.de>