from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


DUCKBURGH = [
    'donald', 'scroogemcduck', 'daisyduck', 'mickeymouse'
]


class ImportHelper(object):
    def post_import(self):
        User = get_user_model()

        for user in DUCKBURGH:
            email = '{}{}'.format(user, '@example.com')
            if not User.objects.filter(email=email).exists():
                User.objects.create(email=email)

        User.objects.all().update(password=make_password('test'))
