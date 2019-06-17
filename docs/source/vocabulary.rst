Vocabulary
==========

Provit uses a small subset of the `W3C <https://www.w3.org/>`__ `PROV-O
vocabulary <https://www.w3.org/TR/prov-o/>`__. 


Agents
------

Provit implements three different agents:

- Organization
- Person
- SoftwareAgent

The names are specified in PROV-O. 

Organization
~~~~~~~~~~~~

An `organizations <https://www.w3.org/TR/2013/REC-prov-o-20130430/#Organization>`__ is a social or legal institution that can be responsible for creation or modification of data (in our case). 

A valid entry for *~/.provit/agents/wikidata.yaml* would be:

.. code:: yaml
        
        homepage:
        - https://www.wikidata.org
        name:
        - Wikidata
        slug: wikidata
        type: Organization

Person
~~~~~~

A `persons <https://www.w3.org/TR/2013/REC-prov-o-20130430/#Person>`__ is a human actor. If a person manually corrects a data set, it is the agent responsible for this modification step.

A valid entry for *~/.provit/agents/johndoe.yaml* would be:

.. code:: yaml

        email:
        - john.doe@uni-leipzig.de
        - doe.john@ub.uni-leipzig.de
        homepage:
        - https://ub.uni-leipzig.de
        - https://diggr.link
        institution:
        - ubleipzig
        name:
        - "John Doe"
        - "J. Doe"
        - "John Dö"
        slug: johndoe
        type: Person


SoftwareAgent
~~~~~~~~~~~~~

A `SoftwareAgent <https://www.w3.org/TR/2013/REC-prov-o-20130430/#SoftwareAgent>`__ is running software (e.g. a scraper for data retrieval or bulk downloader). 

A valid entry for *~/.provit/agents/gephi_0.9.2.yaml* would be:

.. code:: yaml

        homepage:
        - https://gephi.org/
        name:
        - Gephi
        slug: gephi_0.9.2
        type: SoftwareAgent
        version:
        - 0.9.2
