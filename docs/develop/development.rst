##########################
Develop the Django project
##########################

.. note:: You should read :doc:`gettingstarted` before you read this.


.. note::

    All the commands in this guide assumes you have :ref:`enabled the virtualenv
    <enable-virtualenv>`, and that the CWD is the root of the repo.



******************************************************
Run the Django development server with sqlite database
******************************************************
Run::

    $ python manage.py runserver

to start the Django development server.


***********************************************
Run the Django development server with Postgres
***********************************************
Run::

    $ DJANGOENV=postgres_develop python manage.py runserver

to start the Django development server.


*************
Running tests
*************
To run the tests, we need to use a different settings file. We tell mgp to
do this using the ``DJANGOENV`` environent variable::

    $ DJANGOENV=test python manage.py test
