from invoke import task
from os import remove
from os.path import exists, join


SQLITE_DATABASE = 'db.sqlite3'
DUMPSCRIPT_DATAFILE = join(
    'trix', 'project', 'develop', 'dumps', 'dev', 'data.py')


def _manage(ctx, args, env='develop'):
    command = 'python3 manage.py {0} --traceback'.format(args)
    return ctx.run(command, env={'DJANGOENV': env})


@task
def py_version(ctx):
    """
    Runs the python version invoke is run with, python3.
    """
    return ctx.run('python3 --version')


@task
def migrate(ctx):
    """
    Runs the makemigrations and migrate django management commands.
    """
    _manage(ctx, 'makemigrations --noinput')
    _manage(ctx, 'makemigrations --noinput trix_core')
    _manage(ctx, 'migrate --noinput')


@task
def removedb(ctx):
    """
    Remove the database.
    """
    if exists(SQLITE_DATABASE):
        remove(SQLITE_DATABASE)


@task
def resetdb(ctx, env='develop'):
    """
    Remove db.sqlite if it exists, and run the ``migrate`` task.
    """
    if env == 'develop':
        if exists(SQLITE_DATABASE):
            remove(SQLITE_DATABASE)
    else:
        # TODO fix so it works
        _manage('dbdev_reinit')
    migrate(ctx)


@task
def recreate_devdb(ctx):
    """
    Recreate the test database.
    """
    resetdb(ctx)
    _manage(ctx, 'runscript trix.project.develop.dumps.dev.data')


@task
def dump_to_db(ctx):
    """
    Dump current db to the dumpscript dataset.
    """
    dump = _manage(ctx, 'dumpscript trix_core')
    with open(DUMPSCRIPT_DATAFILE, 'wb') as outfile:
        outfile.write(dump.stdout + '\n')


@task
def run_tests(ctx):
    """
    Runs tests under test djangoenv.
    """
    _manage(ctx, 'test', env='test')


# Static tasks #
@task
def npm_install(ctx, gbl=False):
    """
    Run npm install
    """
    with ctx.cd('trix/trix_student/static/trix_student'):
        if (gbl):
            ctx.run('npm install -g')
        else:
            ctx.run('npm install')


@task
def bower_install(ctx):
    """
    Run bower install
    """
    with ctx.cd('trix/trix_student/static/trix_student'):
        ctx.run('bower install')


@task
def grunt_build(ctx):
    """
    Run grunt build
    """
    with ctx.cd('trix/trix_student/static/trix_student'):
        ctx.run('grunt build')


@task
def grunt_watch(ctx):
    """
    Run grunt watch
    """
    with ctx.cd('trix/trix_student/static/trix_student'):
        ctx.run('grunt watch')


# i18n tasks #
@task
def makemessages(ctx, langcode='nb'):
    """
    Runs makemessages for the given locale (default to nb).
    """
    _manage(ctx, 'makemessages -l {} -i "**/static/*"'.format(langcode))


@task
def jsmakemessages(ctx, langcode='nb'):
    """
    Runs makemessages for javascript in the given locale (default to nb).
    """
    _manage(ctx, 'makemessages -d djangojs -l {} -v3 '
            '-i "**/static/**/node_modules/*" '
            '-i "**/static/**/bower_components/**"'.format(langcode))


@task
def compilemessages(ctx):
    """
    Runs compilemessages.
    """
    _manage(ctx, 'compilemessages')
