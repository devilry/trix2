from shutil import rmtree
import os.path
from glob import glob
from fabric.api import local, task


@task
def docs():
    """
    Build the docs.
    """
    apidocdir = os.path.join('django', '_apidoc')
    if os.path.exists(apidocdir):
        rmtree(apidocdir)

    exclude = glob('../trix/*/migrations/') \
        + glob('../trix/*/tests/')
    exclude = map(os.path.abspath, exclude)

    local('sphinx-apidoc -o develop/_apidoc/ --no-toc ../trix {exclude}'.format(
        exclude=' '.join(exclude)
    ))
    local('sphinx-build -b html . _build')
