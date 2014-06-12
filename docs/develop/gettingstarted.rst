############################################################
Getting started with the Django app and/or the documentation
############################################################


************************
Install the requirements
************************
Install the following:

#. Python
#. PIP_
#. VirtualEnv_
#. virtualenvwrapper_
#. libjpeg, liblcms1, libfreetype6 and zlib for the required format support in Pillow
#. gettext for Django translations
#. nodejs and npm for our clientside stuff


Install the system packages on OSX with Homebrew
================================================
::

    $ brew install gettext nodejs

You will also have to add gettext to your path if you want to be able to update translation strings. You can eighter run ``brew link gettext --force``, or add ``/usr/local/Cellar/gettext/SOMETHING/bin/`` to your path.


Install the system packages on Ubuntu
================================================
::

    $ sudo apt-get install gettext nodejs



***********************
Install in a virtualenv
***********************
Create a virtualenv (an isolated Python environment)::

    $ mkvirtualenv lokalt

Install the development requirements::

    $ pip install -r requirements/develop.txt


.. _enable-virtualenv:

.. note::

    Whenever you start a new shell where you need to use the virtualenv we created
    with ``mkvirtualenv`` above, you have to run::

        $ workon lokalt


*****************
Create a database
*****************
See :doc:`databasedumps`.





**************
Build the docs
**************
:ref:`Enable the virtualenv <enable-virtualenv>`, and run::

    $ cd docs/
    $ fab docs

Then open ``_build/index.html`` in a browser.




.. _PIP: https://pip.pypa.io
.. _VirtualEnv: https://virtualenv.pypa.io
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/
