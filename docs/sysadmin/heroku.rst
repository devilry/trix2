####################
Setup Trix on Heroku
####################


***********
Quick setup
***********

Create an Heroku account
========================
Go to https://www.heroku.com and create your Heroku account. Make sure you set it up completely (including setting a SSH key).


Clone the Trix repo
===================
First you need to checkout the Trix repo::

    $ git clone https://github.com/devilry/trix2.git
    $ cd trix2/


Create the Heroku instance
==========================
Next, create the heroku instance. We have configured everything for Heroku, so all you need is::

    $ heroku create
    $ heroku config:set DJANGOENV=production
    $ heroku config:set DJANGO_SETTINGS_MODULE=trix.project.settingsproxy
    $ git push heroku master
    $ heroku ps:scale web=1


.. note::

    You can create the Heroku instance in Europe with::

        $ heroku create --region eu

.. note::

    The Heroku config for Trix is basically the same as the one
    in https://devcenter.heroku.com/articles/getting-started-with-django.


.. _herokucreatedemodb:

Create a demo database
======================
To create the Trix demo database, run::

    $ heroku run bash
    >$ python manage.py syncdb --noinput
    >$ python manage.py migrate --noinput
    >$ python manage.py runscript trix.project.develop.dumps.dev.data
    >$ exit


Drop and recreate the database
==============================
If you need to drop and recreate the database, run::

    $ heroku pg:info

You will find database name on the first line (all uppercase, something like HEROKU_POSTGRESQL_AQUA_URL). Then you can run::

    $ heroku pg:reset <database-name>

Lastly, repeat herokucreatedemodb_.
