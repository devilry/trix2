from invoke import task


@task
def docs(ctx):
    """
    Build the docs.
    """
    ctx.run('sphinx-build -b html . _build')
