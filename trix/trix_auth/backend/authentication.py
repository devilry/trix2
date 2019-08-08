

class TrixAuthenticationBackend(object):

    def authenticate(self, request, username=None, password=None):
        return

    def has_perm(self, user_obj, perm, obj=None):
        print("\nHERE\n")
        return False
