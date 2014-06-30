from django.contrib.auth import get_user_model


def create_user(email, password='test', **kwargs):
    """
    Create a user with the given ``email``.

    :param email: The ``email`` of the user.
    :param password: Defaults to ``test``.
    :param kwargs: Extra attributes for :class:`trix.trix_core.models.User`.

    Examples::

        from trix.project.develop.testhelpers.user import create_user
        myuser = create_user('myuser', fullname="My User")
    """
    user = get_user_model().objects.create(email=email, **kwargs)
    user.set_password(password)
    user.save()
    return user
