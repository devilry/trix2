#########################
Setup Trix for production
#########################


********************
Install dependencies
********************
#. Python 2.7.X. Check your current version by running ``python --version``.
#. PIP_
#. VirtualEnv_
#. PostgreSQL server --- not needed if you just want to build the docs.


************************************************************
Create or select a user that you want to run the Trix server
************************************************************
We recommend using a normal user with no admin/root/sudo privileges to run Trix.
You should perform the rest of the steps in this guide as this new user.


********************************************
Make a directory where you will install trix
********************************************
This directory MUST NOT be served by a http server like apache. It should be a well protected
local directory only acceccible to the user running Trix. Example::

    $ mkdir ~/trixdeploy

We will refer to your trix deploy directory as ``~/trixdeploy`` for the rest of this guide.



************
Install Trix
************
::

    $ cd ~/trixdeploy
    $ virtualenv venv
    $ venv/bin/pip install psycopg2 dj-static trix


*********************************
Create a Django management script
*********************************
Copy this script into ``~/trixdeploy/manage.py``::

    import os
    import sys

    if __name__ == "__main__":
        os.environ["DJANGO_SETTINGS_MODULE"] = "trix_settings"
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)

Just to make sure everything works, run it with::

    $ cd ~/trixdeploy/
    $ venv/bin/python manage.py syncdb --noinput

This should create a file named ``~/trixdeploy/trixdb.sqlite``. You can remove that file now - it was just for testing.


*********
Configure
*********
Trix is configured through a ``trix_settings.py`` file. Start by copying the following into
``~/trixdeploy/trix_settings.py``::

    TODO


********************
Configure a database
********************
Configure a Postgres database by editing the ``DATABASE_URL`` setting in your ``trix_settings.py`` script. The format is::

    postgres://USER:PASSWORD@HOST:PORT/NAME


**********************
Configure a SECRET_KEY
**********************
Configure the SECRET_KEY (used for cryptographic signing) by editing the ``SECRET_KEY`` setting in your
``trix_settings.py`` script. Make it a 50 characters long random string. Example (**DO NOT COPY**)::

    SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


******************
Disable debug mode
******************
Before running Trix in production, you **must** set ``DEBUG=False`` in ``trix_settings.py``.

.. warning::

    If you do not disable DEBUG mode in production, you database credentials and SECRET_KEY
    will be shown to any visitor when they encounter an error.


*************************
Run the production server
*************************
::

    DJANGO_SETTINGS_MODULE=trix_settings gunicorn trix.project.production.wsgi -b 0.0.0.0:8000 --workers=12 --preload

You can adjust the number of worker threads in the ``--workers`` argument,
and the port number in the ``-b`` argument. You can run this on port 80,
but if you want to have SSL support, you will need to use a HTTP proxy
server like Apache og Nginx.


.. _PIP: https://pip.pypa.io
.. _VirtualEnv: https://virtualenv.pypa.io
