##########################
Git_ usage in this project
##########################

- Commit often, and with good messages. 

- Commit messages should allways start with a prefix of where changes have been made. Example:

	- *djangoproject: Added login view, with redirect to reset password if user does not exist in django auth.*

	- *docs: Added description of how to use postgres as development db.*


- Throw your local changes

	* If you want to revert changes made to your working copy, do this: ``git checkout .``

	* If you want to revert changes made to the index (i.e., that you have added), do this: ``git reset``

	* If you want to revert a change that you have committed, do this: ``git revert ...``


.. _Git: http://git-scm.com/
.. _`reStructuredText Primer`: http://sphinx.pocoo.org/rest.html
