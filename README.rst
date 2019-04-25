PROVIT - PROVenance Integration Tools
=======================================

|Python 3.6| |GitHub license| |GitHub issues| |Docs passing|

PROVIT is a light, dezentralized data provenance and documentation tool. It allows
the user to track workflows and modifications of data-files. 

PROVIT works completely decentralized, all information is stored in .prov
files (as JSON-LD RDF graphs) along it's corresponding data file in the file system.
No additional database or server setup is needed.  

A small subset of the `W3C <https://www.w3.org/>`__ `PROV-O
vocabulary <https://www.w3.org/TR/prov-o/>`__ is implemented. 

PROVIT aim to provided an easy to use interface for users who have never worked with provenance
tracking before. If you feel limited by PROVIT you should have a look at
more extensive implementations, e.g.: `prov <https://github.com/trungdong/prov/>`__.

Full documentation is available under: `provit.readthedocs.io <https://provit.readthedocs.io/en/latest/>`__.


Requirements
------------

This software was tested on Linux with Python 3.5 and 3.6.

Installation
------------

Installation via `pip <https://pypi.org/>`__ is recommended for end
users. We strongly encourage end users to make use of a
`virtualenv <https://virtualenv.pypa.io/en/stable/>`__.

pip
~~~

Clone the repository and create a virtual environment (optional) and 
install into with pip into the virtualenv.

.. code:: zsh

    $ mkvirtualenv provit
    $ pip install provit

git / Development
~~~~~~~~~~~~~~~~~

Clone the repository and create a virtualenv.

.. code:: zsh

    $ git clone https://github.com/diggr/provit
    $ mkvirtualenv provit

Install it with pip in *editable* mode

.. code:: zsh

    $ pip install -e ./provit

Usage
-----

PROVIT provides a command line client which can be
used to enrich any file based data with provenance
information. 

PROVIT also includes a (experimental) web-based interface 
(PROVIT Browser).


Command Line Client
~~~~~~~~~~~~~~~~~~~

Usage:

Open PROVIT Browser:

.. code:: zsh

    $ provit browser

Add provenace event to a file:

.. code:: zsh

    $ provit add FILEPATH [OPTIONS]

Options:

-a AGENT, --agent AGENT    Provenance information: agent (multiple=True)
--activity ACTIVITY        Provenance information: activity
-d DESCRIPTION, --desc DESCRIPTION     Provenance information: Description
                            of the data manipulation process
-o ORIGIN, --origin ORIGIN    Provenance information: Data origin
-s SOURCES, --sources SOURCES    Provenance information: Source files (multiple=True)
--help      Show this message and exit.

Provenance Class
~~~~~~~~~~~~~~~~

.. code:: python

    from provit import Provenance

    # load prov data for a file, or create new prov for file
    prov = Provenance(<filepath>)

    # add provenance metadata
    prov.add(agents=[ "agent" ], activity="activity", description="...")
    prov.add_primary_source("primary_source")
    prov.add_sources([ "filepath1", "filepath2" ])

    # return provenance as json tree
    prov_dict = prov.tree()

    # save provenance metadata into "<filename>.prov" file
    prov.save()

Roadmap
-------

General roadmap of the next steps in development

- Tests
- Tutorials
- Windows support
- Agent management in PROVIT Browser

Overview
--------

:Authors:
    P. Mühleder muehleder@ub.uni-leipzig.de,
    F. Rämisch raemisch@ub.uni-leipzig.de
:License: MIT
:Copyright: 2018, Peter Mühleder and `Universitätsbibliothek Leipzig <https://ub.uni-leipzig.de>`__

.. |Python 3.6| image:: https://img.shields.io/badge/Python-3.6-blue.svg
.. |GitHub license| image:: https://img.shields.io/github/license/diggr/pit.svg
   :target: https://github.com/diggr/pit/blob/master/LICENSE
.. |GitHub issues| image:: https://img.shields.io/github/issues/diggr/pit.svg
   :target: https://github.com/diggr/provit/issues
.. |Docs passing| image:: https://readthedocs.org/projects/provit/badge/?version=latest
   :target: http://provit.readthedocs.io/en/latest/?badge=latest
