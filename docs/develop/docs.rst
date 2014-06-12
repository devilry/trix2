############################
Adding to this documentation
############################

This documentation uses Sphinx_. It is generated from the reStructuredText
sources in ``docs/*.rst``. See `reStructuredText Primer`_ for to learn
reStructuredText (very easy to learn the basics).

*********************
How to build the docs
*********************
This is explained in ``README.md`` at the root of the git repo.


*****************************************
How to add a new file to the documenation
*****************************************
- Add a new ``.rst``-file in ``docs/<subdirectory>/``, where ``<subdirectory>``
  is the part of the project where the new document belongs.
- Add the filename without .rst to a toctree in
  ``docs/<subdirectory>/index.rst``


*****************************************
Language and file naming
*****************************************
- Write everything in English.
- Use english lowercase letters and no spaces to name the ``.rst``-files. Use ``-`` or ``_`` instead of spaces.


******************************************
Linking to issues and wiki pages on github
******************************************
You can link to issues and wiki pages using the following syntax::

    :issue:`<issue number>`
    :wikipage:`<page name>`

E.g.::

    :issue:`10`
    :wikipage:`SomePage`

This is handled by the `extlinks Sphinx extension`_


.. _Sphinx: http://sphinx.pocoo.org/
.. _`reStructuredText Primer`: http://sphinx.pocoo.org/rest.html
.. _`extlinks Sphinx extension`: http://sphinx-doc.org/ext/extlinks.html