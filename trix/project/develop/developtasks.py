from fabric.api import task, local
from fabric.context_managers import shell_env
from os import remove
from os.path import exists, join


SQLITE_DATABASE = 'db.sqlite3'
DUMPSCRIPT_DATAFILE = join(
    'trix', 'project', 'develop', 'dumps', 'dev', 'data.py')


def _manage(args, capture=False):
    command = 'python manage.py {0} --traceback'.format(args)
    return local(command, capture=capture)


@task
def syncmigrate(djangoenv='develop'):
    """
    Runs the syncdb and migrate django management commands.
    """
    with shell_env(DJANGOENV=djangoenv):
        _manage('syncdb --noinput')
        _manage('migrate --noinput')


@task
def removedb():
    """
    Remove the database.
    """
    if exists(SQLITE_DATABASE):
        remove(SQLITE_DATABASE)


@task
def resetdb(djangoenv='develop'):
    """
    Remove db.sqlite if it exists, and run the ``syncmigrate`` task.
    """
    if djangoenv == 'develop':
        if exists(SQLITE_DATABASE):
            remove(SQLITE_DATABASE)
    else:
        with shell_env(DJANGOENV=djangoenv):
            _manage('dbdev_reinit')
    syncmigrate(djangoenv)


@task
def recreate_devdb(djangoenv='develop'):
    """
    Recreate the test database.
    """
    resetdb(djangoenv)
    with shell_env(DJANGOENV=djangoenv):
        _manage('runscript trix.project.develop.dumps.dev.data')


@task
def dump_current_db_to_dumpscript_datafile():
    """
    Dump current db to the dumpscript dataset.
    """
    dump = _manage('dumpscript trix_core', capture=True)
    with open(DUMPSCRIPT_DATAFILE, 'wb') as outfile:
        outfile.write(dump + '\n')
