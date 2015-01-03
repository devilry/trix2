#############################
Add a new timeperiod/semester
#############################

The active timeperiod/semester within a course is defined as a tag with the *period* category. Administrators can
access all assignments tagged with a course where they have administrator rights, but students can only access
assignments tagged with the active period tag configured for a course.

.. note::
    This is very powerful, since publishing/unpublishing assignments only require an
    administrator to remove/add the active period tag from an assignment.


To add a new period tag, go to ``/admin/``:

.. image:: ../images/djangoadmin_frontpage.png

Click the **Tags** item in the list:

.. image:: ../images/tags_list.png

Click **Add Tag** in the upper right corner and then type the name of the tag along with the category *Period*.

The newly added period tag can then be defined as the active period on a course.
