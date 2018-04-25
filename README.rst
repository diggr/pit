P(ROV)IT - PROVenance integration tools
=======================================

|Python 3.6| |GitHub license| |GitHub issues|

PROVIT is a light, dezentralized provenance tracking framework. It allows
the user to track workflows and modifications of data and files. A
small subset of the `W3C <https://www.w3.org/>`__ `PROV-O
vocabulary <https://www.w3.org/TR/prov-o/>`__ is implemented. Its aim is to
provided an easy to use interface for users who have never worked with provenance
tracking before. It you feel limited by PROVIT you should have a look at
the more extensive implementation `prov <https://github.com/trungdong/prov/>`__.

Requirements
------------

This Software was tested with Python 3.5 and 3.6.

Installation
------------

Installation via `pip <https://pypi.org/>`__ is recommended for end
users. We strongly encourage end users to make use of a
`virtualenv <https://virtualenv.pypa.io/en/stable/>`__.

pip
~~~

Clone the repository and create a virtualenv.

.. code:: zsh

    $ git clone https://github.com/diggr/pit
    $ mkvirtualenv provit

Install it with pip

.. code:: zsh

    $ pip install PATH_TO_PROVIT_REPOSITORY

git / Development
~~~~~~~~~~~~~~~~~

Clone the repository and create a virtualenv.

.. code:: zsh

    $ git clone https://github.com/diggr/pit
    $ mkvirtualenv provit

Install it with pip in *editable* mode

.. code:: zsh

    $ pip install -e PATH_TO_PROVI_REPOSITORY

Usage
-----

Provenance Integration Tools provide a command line client which can be
used *out of the box* to enrich any file based data with provenance
information. Furthermore the provenance class and vocabulary shipped
with *PIT* can be used within other applications.

Command Line Client
~~~~~~~~~~~~~~~~~~~

Usage:

.. code:: zsh

    $ pit [OPTIONS] FILEPATH

Options:

--add                       Add provenance information layer to file
-a, --agent=TEXT            Provenance information: agent
--activity=TEXT             Provenance information: activity
-d, --desc=TEXT             Provenance information: Description
                            of the data manipulation process
-o, --origin=TEXT           Provenance information: Data origin
-s, --sources=TEXT          Provenance information: Source files
-b, --browser               Provenance browser
-n, --namespace=TEXT        Provenance Namespace,
                            default: http://provit.diggr.link/
--help                      Show this message and exit.

Provenance Class
~~~~~~~~~~~~~~~~

.. code:: python

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

Roadmap
-------

General Roadmap containing features we'd like to realize in the project

- Add Persons to Agent, to allow more granular activity tracking

Feature Wishlist
~~~~~~~~~~~~~~~~

A more detailed list of specific (smaller) features and functionality.

Notify user if source referenced file changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Provenance files contain the version of a file if referenced, if an
older version (i.e. not the current version) of a file is referenced, a
warning should be displayed.

File Browser
^^^^^^^^^^^^

A file browser showing e.g. all files with missing provenance.

Reference Clustering
^^^^^^^^^^^^^^^^^^^^

Inspect files in your *research* folder, and display all references, to
identify clusters. This could help structuring a messy research
directory without breaking scripts, or at least knowing, which scripts
possibly need to be updated.

FAQ / Paradigms
---------------

Can I add multiple agents to an activity?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No. The reason is: If you can distinguish the activities or impact of
the agent, then you have multiple agents with *multiple activities*.
E.g. if you let three students help you proofreading a file and you get
back *1* revised version, then the three students are *1 agent* as you
cannot distinguish between their results. If you get back *3 versions*
you have *3 agents* and *3 activities*.

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
   :target: https://github.com/diggr/pit/issues
