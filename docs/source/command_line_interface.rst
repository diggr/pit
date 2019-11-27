provit command line interface
=============================

Provenance information can be inspected and created using the command line interface.
A short demonstration of the capabilities is given below.

.. image:: assets/provit_demo_001.gif

Show Provenance
---------------

To show the provenance information for a file *cd* into the directory and enter the show 
command.

.. code:: zsh

        $ provit show source_file
        {
            "uri": "http://vocab.ub.uni-leipzig.de/provit/source_file/0cab498f56e3417da1120dcaa6f48354",
            "agent": [
                "http://vocab.ub.uni-leipzig.de/provit/enrich_0.1.0"
            ],
            "activity": "http://vocab.ub.uni-leipzig.de/provit/data_download/632c7e1fb1814cda86d7c727f1b1a4ed",
            "ended_at": "2019-11-27 15:01:48",
            "activity_desc": "The data was downloaded",
            "location": "/home/fraemisch/tmp/provit_demo/source_file",
            "primary_sources": [
                "http://vocab.ub.uni-leipzig.de/provit/https:/diggr.link"
            ],
            "sources": []
        }


Create Provenance (interactively)
---------------------------------

Provenance information can be appended to existing provenance information or 
created for files, which do not yet have provenance information attached.

The following command will take you to the interactive prompt which guides you through 
the provenance creation process.

.. code:: zsh
        
        $ provit create FILENAME

.. note::
        
        Agents can not be created properly using this interface. Please see :doc:`vocabulary` for 
        information on the types of agents and how to create them.


Create Provenance (non-interactive)
-----------------------------------

Sometimes you want to create provenance by just giving the information as command line 
arguments. This is also possible, but should only be used by advanced users or in scripts.

.. code:: zsh

        provit add \
                --agent testagent \
                --comment test \
                --activity testing \
                FILENAME

This will create a *FILENAME.prov* file right next to your existing data file, or append the provenance information given as options to the provenance graph, in case the file already exists.

~/.provit directory
-------------------

*provit* stores information about agents and its configuration in the home 
directory. You can 

Have a look at the :doc:`vocabulary` section to see example agent files. 
