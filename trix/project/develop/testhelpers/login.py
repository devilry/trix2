
class LoginTestCaseMixin(object):
    """
    Mixin class for TestCase that makes it easy to test views as an authenticated user.

    Example::

        from django.test import TestCase
        from trix.project.develop.testhelpers.login import LoginTestCaseMixin
        from trix.project.develop.testhelpers.user import create_user

        class TestSomeView(TestCase, LoginTestCaseMixin):

            def test_something(self):
                someuser = create_user('someuser')
                response = self.get_as(someuser, '/some/url')

    """
    def login(self, user, password='test'):
        """
        Login the given ``user``.
        """
        self.client.login(email=user.email, password=password)

    def get_as(self, user, *args, **kwargs):
        """
        Just like ``client.get(...)``, except that the first argument is
        the user you want to login as before performing the GET request.
        """
        self.login(user)
        return self.client.get(*args, **kwargs)

    def post_as(self, user, *args, **kwargs):
        """
        Just like ``client.post(...)``, except that the first argument is
        the user you want to login as before performing the POST request.
        """
        self.login(user)
        return self.client.post(*args, **kwargs)

    def delete_as(self, user, *args, **kwargs):
        """
        Just like ``client.delete(...)``, except that the first argument is
        the user you want to login as before performing the DELETE request.
        """
        self.login(user)
        return self.client.delete(*args, **kwargs)

    def put_as(self, user, *args, **kwargs):
        """
        Just like ``client.put(...)``, except that the first argument is
        the user you want to login as before performing the PUT request.
        """
        self.login(user)
        return self.client.put(*args, **kwargs)
