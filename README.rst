Regolith Helpers
****************

Helper functions for adding things to regolith databases and making reports

Proper builders should be added directly to regolith,
but quicker hacky things can go here

Installation
============
#. fork and clone the repository
#. cd to directory with setup.py in it
#. activate your conda env where you do regolith work
#. type ``python setup.py develop``
#. test your installation ``rh -h`` should return a help message

Usage
=====
#. in a terminal window, navigate to the relevant directory for your work.
   This could be ``rg-db-private/local``, ``rg-db-group/local``, or
   ``rg-db-public/local`` depending which database you want to update or query
#. type ``rh --help`` to see what helpers are available
#. type ``rh <helper-name> --help`` to see what the helpers do as well as
   getting a list of all the positional (required)
   and optional command line arguments that should/can be specified
#. type ``rh <helper-name> pos1value pos2value --cond1 cond1value --cond2 cond2value``
   where the pos1value is the value you want to give the first positional argument
   of the helper, and so on.
#. helpers sometimes update databases by inputting data, or they print
   information to screen for quick assessment of something, or they produce an
   output file that will be in the ``./_build/<helper-name>`` directory, relative
   to the directory where you are running it

Example:
========

``rh a_proprev --help`` produces
 .. code-block:: python

    usage: rh a_proprev [-h] [-q REQUESTER] [-r REVIEWER] [-s STATUS] [-t TITLE]
                        name type due_date

    positional arguments:
      name                  pi first name space last name in quotes
      type                  nsf or doe
      due_date              due date in form YYYY-MM-DD

    optional arguments:
      -h, --help            show this help message and exit
      -q REQUESTER, --requester REQUESTER
                            Name of the Program officer requesting
      -r REVIEWER, --reviewer REVIEWER
                            name of the reviewer. Defaults to sbillinge
      -s STATUS, --status STATUS
                            status, from [invited, accepted, declined,
                        downloaded,inprogress, submitted], default is accepted
      -t TITLE, --title TITLE
                        the title of the proposal

so you may type something like
 .. code-block:: python

    usage: rh a_proprev "A. Einstein" nsf 1905-05-10 -t "towards a theory of relativity" -q "P. O. Officer" -s downloaded -r me

to add to the proposalReviews collection a new entry for a proposal you have been sent to review by a Program Office with the name P. O. Officer with a due date of 10th May 1905