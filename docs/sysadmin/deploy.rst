#########################
Setup Trix for production
#########################


********************
Install dependencies
********************
#. Python 3.8 or higher. Check your current version by running ``python --version``.
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
    $ venv/bin/pip3 install psycopg2 trix


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


*********
Configure
*********
Trix is configured through a ``trix_settings.py`` file. Start by copying the following into
``~/trixdeploy/trix_settings.py`` and replace the database placeholders with your own::

    from trix.project.production.settings import *

    # Make this 50 chars and RANDOM - do not share it with anyone
    SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    # Database config
    DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DATABASE_NAME',
        'USER': 'DATABASE_USERNAME',
        'PASSWORD': 'DATABASE_PASSWORD',
        'HOST': 'DATABASE_HOST',
        'PORT': '5432',
        'OPTIONS': {
          'sslmode': 'require',
        },
      }
    }

    # Set this to False to turn of debug mode in production
    DEBUG = False

****
LDAP
****
To enable LDAP authenication, ``trix_settings.py`` would need to include an authenication backend
with LDAP support, the URI for the LDAP server and its DN template, and possiblely some
`customization <https://django-auth-ldap.readthedocs.io/en/latest/authentication.html#customizing-authentication>`_
to adjust for how the usernames are stored in Trix's database.

As an example, the settings for UiO would need to adjust for the LDAP username not being a full
email adresse by overwriting ``ldap_to_django_username()`` and ``django_to_ldap_username()``
functions of ``django_auth_ldap.backend.LDAPBackend``.

Add the following to you ``trix_settings.py`` file (but adjust the DN template)::

    AUTHENTICATION_BACKENDS = [
        'trix_uio_ldap_auth.TrixUioLDAPBackend',
    ]
    AUTH_LDAP_SERVER_URI = 'ldaps://ldap.uio.no'
    AUTH_LDAP_USER_DN_TEMPLATE = 'uid=hei,cn=people,dc=uio,dc=no'

Create a ``trix_uio_ldap_auth.py`` as follows (but adjust the email suffix)::

    from django_auth_ldap.backend import LDAPBackend

    class TrixUioLDAPBackend(LDAPBackend):
        def ldap_to_django_username(self, username):
            return '{}@example.com'.format(username)

        def django_to_ldap_username(self, username):
            return username.split('@')[0]



***********
Federated authentication
***********
Trix has build-in support for replacing the login using OpenID Connect (OIDC) with Feide (through
Dataporten) and/or other OIDC-compliant identify providers through Keycloak. If two or more
providers are configured the user will be asked to select one of the available providers before
they are redirected.

Steps to enable Feide login:
#. Register a new `Dataporten Application <https://dashboard.dataporten.no/>`_. Documentation can
be found in their `Dataporten docs <https://docs.feide.no/developer_oauth/register_and_manage_applications/getting_started_app_developers.html>`_.
Use the redirect URL ``http://<webpage URL>:<port>/authenticate/allauth/dataporten/login/callback/``

#. Add the provider details to your ``trix_settings.py`` file using by overwriting
``SOCIALACCOUNT_PROVIDERS`` (default: ``None``)::

    SOCIALACCOUNT_PROVIDERS = {
        'dataporten': {
            'APPS': [
                {
                    'client_id': 'TRIX_DATAPORTEN_CLIENT_ID',
                    'secret': 'TRIX_DATAPORTEN_SECRET',
                }
            ]
        }
    }

Optional settings for logout URLs and validating the response can be provided separately::

    SOCIALACCOUNT_EXPECTED_RESPONSES = {
        'dataporten': {"userid": "", "email": "", "userid_sec": []},
    }
    
    SOCIALACCOUNT_LOGOUT_URLS = {
        'dataporten': 'https://auth.dataporten.no/logout',
    }


#. Login and logout should now work through Dataporten. Users will still be created and can be
edited as normal.

In a similar fashion, Keycloak can be enabled using `Allauth's OpenID Connect provider <https://docs.allauth.org/en/latest/socialaccount/providers/keycloak.html>`_::

    SOCIALACCOUNT_PROVIDERS = {
        'dataporten': {
            (...)
        },
        'openid_connect': {
            'APPS': [
                {
                    'provider_id': 'keycloak',
                    'name': 'Displayed when choosing between providers',
                    'client_id': 'TRIX_KEYCLOAK_CLIENT_ID',
                    'secret': 'TRIX_KEYCLOAK_SECRET',
                    'settings': {
                        'server_url': 'http://keycloak:8080/realms/master/.well-known/openid-configuration',
                    },
                }
            ],
            'SCOPES': ['email', 'openid', 'profile']
        }
    }
    
    SOCIALACCOUNT_LOGOUT_URLS = {
        'keycloak': 'URL_TO_END_SESSION_ENDPOINT',
    }


****************
Consent template
****************
Customising the consent template is highly recommended and can be done by following these steps:

#. Create a directory for custom templates with a subfolder named ``trix_student``
#. Create a django html file called ``consent_form.django.html`` and make it look like this::

    {% extends "trix_student/consent_form_base.django.html" %}

    {% block consent_title %}<h1>Consent title here</h1>{% endblock %}

    {% block consent_text %}Lorem Ipsum{% endblock %}

    {# If you want to override the buttons you can add this #}
    {# {% block consent_buttons %}BUTTONS{% endblock %} #}


#. In ``trix_settings.py`` do::

    from trix.utils.template import add_custom_template

    add_custom_template('custom_template_directory/goes/here')

If you wish to disable the consent dialog completely for some reason, add ``DISABLE_CONSENT = True``
to your ``trix_settings.py`` file.


****************
Footer template
****************
Customize the footer template to contain your own information

#. Create a directory for custom templates with a subfolder named ``trix_student``
#. In ``trix_student`` create a subfolder named ``include``
#. Create a django html file called ``footer.django.html`` and make it look like this::

    {% extends "trix_student/include/footer_base.django.html" %}
    {% load i18n %}

    {% block body %}
        <span class="fa fa-bug"></span>
        <a href="report url" target="_blank">
            {% trans "Report bug" %}
        </a>

        <span class="fa fa-question"></span>
        <a href="link1">{% trans "Help" %}</a>

        <span class="fa fa-info"></span>
        <a href="link2">{% trans "Privacy" %}</a>

        <span class="fa fa-info"></span>
        <a href="version url">Trix v{{ TRIX_VERSION }}<a>
    {% endblock %}


******************
Make sure it works
******************
Just to make sure everything works, run::

    $ cd ~/trixdeploy/
    $ venv/bin/python manage.py migrate


********************
Collect static files
********************
Run the following command to collect all static files (CSS, javascript, ...) for Trix::

    $ venv/bin/python manage.py collectstatic

The files are written to the ``staticfiles`` sub-directory (~/trixdeploy/staticfiles).


**********************
Configure a SECRET_KEY
**********************
Configure the SECRET_KEY (used for cryptographic signing) by editing the ``SECRET_KEY`` setting in your
``trix_settings.py`` script. Make it a 50 characters long random string.


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

    $ DJANGO_SETTINGS_MODULE=trix_settings venv/bin/gunicorn trix.project.production.wsgi -b 0.0.0.0:8000 --workers=12 --preload

You can adjust the number of worker threads in the ``--workers`` argument,
and the port number in the ``-b`` argument. You can run this on port 80,
but if you want to have SSL support, you will need to use a HTTP proxy
server like Apache og Nginx.


.. _PIP: https://pip.pypa.io
.. _VirtualEnv: https://virtualenv.pypa.io
