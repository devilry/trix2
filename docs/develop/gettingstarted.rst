############################################################
Getting started with the Django app and/or the documentation
############################################################


************************
Install the requirements
************************
Install the following:

#. Python2.7
#. PIP_
#. VirtualEnv_
#. virtualenvwrapper_
#. gettext for Django translations
#. nodejs and npm for our clientside stuff
.. #. libjpeg, liblcms1, libfreetype6 and zlib for the required format support in Pillow


Install the system packages on OSX with Homebrew
================================================
::

    $ brew install npm nodejs

You will also have to add gettext to your path if you want to be able to update translation strings. You can either run ``brew link gettext --force``, or add ``/usr/local/Cellar/gettext/SOMETHING/bin/`` to your path.


Install the system packages on Ubuntu
================================================
::

    $ sudo apt-get install npm nodejs



***********************
Install in a virtualenv
***********************
Create a virtualenv (an isolated Python environment)::

    $ mkvirtualenv trix


.. _enable-virtualenv:

.. note::

    Whenever you start a new shell where you need to use the virtualenv we created
    with ``mkvirtualenv`` above, you have to run::

        $ workon trix

Install the development requirements::

    $ pip install -r requirements/develop.txt


Run npm install (include -g if you want global)::

    $ inv npm-install


Run bower install::

    $ inv bower-install


Finally build the static files::

    $ inv grunt-build


*****************
Create a database
*****************
See :doc:`databasedumps`.



**************
Build the docs
**************
:ref:`Enable the virtualenv <enable-virtualenv>`, and run::

    $ cd docs/
    $ inv docs

Then open ``_build/index.html`` in a browser.


.. _PIP: https://pip.pypa.io
.. _VirtualEnv: https://virtualenv.pypa.io
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/
