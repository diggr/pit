provit command line interface
=============================

Provenance information can be added using the command line interface.

To do that, *cd* to your data directory and invoke the *provit* cli on any data file
you like.

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
