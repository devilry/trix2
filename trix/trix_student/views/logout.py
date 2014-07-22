from django.contrib.auth.views import logout


def logoutview(request):
    return logout(request, template_name='trix_student/logout.django.html')
