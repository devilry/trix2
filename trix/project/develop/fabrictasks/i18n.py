from fabric.api import task

from .common import root_develop_managepy


@task
def makemessages(langcode='nb'):
    """
    Runs /path/to/reporoot/manage.py makemessages for the given locale (default to nb).
    """
    root_develop_managepy('makemessages -l {} -i "static/*"'.format(langcode))


@task
def jsmakemessages(langcode='nb'):
    """
    Runs /path/to/reporoot/manage.py makemessages for javascript in the given locale (default to nb).
    """
    root_develop_managepy(
        ('makemessages -d djangojs -l {} -v3 '
         '-i "static/**/node_modules/*" '
         '-i "static/**/bower_components/*"').format(langcode))


@task
def compilemessages():
    """
    Runs /path/to/reporoot/manage.py compilemessages.
    """
    root_develop_managepy('compilemessages')
