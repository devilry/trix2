====================================
How to release a new Trix2 version
====================================

- Draft a `Github release <https://github.com/devilry/trix2/releases>`_ and keep updating it with all changes until you're ready to release.
- Update ``trix/version.py``.
- Build: ``$ python setup.py sdist``
- Release to PyPI: ``$ twine upload dist/trix2-<version>.tar.tz``
- Upload the same binaries to the release draft, and click Publish release.
