provit - Provenance Integration Tools
=====================================

|Python 3| |GitHub license| |GitHub issues| |Docs passing|

*provit* is a data provenance annotation and documentation tool. It provides various feature for
creation and retrieval of provenance information for data stored in files. The tracking of sources, 
modifications and merges allows the user to keep a log of all modifications a dataset was subject
to. This is especially useful for dataset which are accessed intermittently or part of a long 
running workflow (e.g. for a scientific thesis). Furthermore, provenance data stored next to the 
data in an archive can help others to identify quality, value and acutality of the data. 

*provit* does not require any external infrastructure. All information is stored in *.prov* 
files right next to the data files as a JSON-LD graph. This makes it the perfect tool for small 
teams or individual researchers. 

To allow interoperatibility, a small subset of the `W3C <https://www.w3.org/>`__ `PROV-O
vocabulary <https://www.w3.org/TR/prov-o/>`__ is implemented. Therefore, the provenance 
information can easily be merge in a linked data graph if necessary, at a later stage of the project.

*provit* aims to provided an easy to use interface for users who have never worked with provenance
tracking before. You can operate the tool using the 

If you feel limited by PROVIT you should have a look at
more extensive implementations, e.g.: `prov <https://github.com/trungdong/prov/>`__.

Full documentation is available under: `provit.readthedocs.io <https://provit.readthedocs.io/en/latest/>`__.

.. image:: assets/provit_promo.png

Quick Installation
------------------

.. note::
   *provit* requires a working installation of Python 3.7, furthermore the use of a 
   `virtualenv <https://virtualenv.pypa.io/en/stable/>`__ is strongly encouraged.
   If you need help to set this up, please follow the Installation section in the documentation. 

*provit* is availabe via the Python Package Index (PyPI) and can be installed by using
pip `pip <https://pypi.org/>`__. Simply create a virtualenvironment with your 
preferred method a run the *pip install* command:

.. code:: zsh

    $ mkvirtualenv provit
    $ pip install provit

Quickstart
----------

*provit* provides three modes of interaction:

* command line interface 
* graphical user interface 
* python package

All of them allow you to track provenance, but the *provit browser* 
additionally lets you explore tracked provenance.

provit browser
~~~~~~~~~~~~~~

You can start provit browser directly from your terminal:

.. code:: zsh

    $ provit browser

provit cli
~~~~~~~~~~

Simply *cd* to the directory, where your data is located, create (or append to an already existing) provenance file. 

.. code:: zsh

    $ provit add FILEPATH [OPTIONS]

The --help command shows you the full list of available options and arguments.

.. code:: zsh

    $ provit --help

provit package
~~~~~~~~~~~~~~~~

Using provit in your ETL pipeline is easy. simply import the Proveance class
and start using it (e.g. as displayed below).

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

We have a small roadmap, which we will make transparent below:

* Increase test coverage (currently 81%)
* Windows support (all devs are on Linux)
* Agent management in PROVIT Browser 

Overview
--------

:Authors:
    P. Mühleder muehleder@ub.uni-leipzig.de,
    F. Rämisch raemisch@ub.uni-leipzig.de
:License: MIT
:Copyright: 2018-2019, Peter Mühleder and `Universitätsbibliothek Leipzig <https://ub.uni-leipzig.de>`__

.. |Python 3| image:: https://img.shields.io/badge/python-3.7-blue.svg
.. |GitHub license| image:: https://img.shields.io/github/license/diggr/pit.svg
   :target: https://github.com/diggr/pit/blob/master/LICENSE
.. |GitHub issues| image:: https://img.shields.io/github/issues/diggr/pit.svg
   :target: https://github.com/diggr/provit/issues
.. |Docs passing| image:: https://readthedocs.org/projects/provit/badge/?version=latest
   :target: http://provit.readthedocs.io/en/latest/?badge=latest
