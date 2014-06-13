import os
import os.path
from fabric.api import local


def is_reporoot(path):
    """
    Return True if the given ``path`` is the root of the Trafo repository.
    """
    return '.this_is_the_trix_reporoot' in os.listdir(path)


def get_reporoot_path():
    """
    Get the repository root path.
    """
    path = os.getcwd()
    while True:
        if is_reporoot(path):
            return os.path.abspath(path)
        newpath = os.path.dirname(path)
        if newpath == path:
            break # Break on /
        path = newpath

    raise ValueError('The CWD is not in the Trix repository.')


def root_develop_managepy(command):
    managepy = os.path.join(get_reporoot_path(), 'manage.py')
    local('python {} {}'.format(managepy, command))
