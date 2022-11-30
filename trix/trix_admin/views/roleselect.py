from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied

from cradmin_legacy.views import roleselect


class TrixRoleSelectView(roleselect.RoleSelectView):
    pagetitle = _('Select a course')
    template_name = 'trix_admin/roleselect.django.html'
    autoredirect_if_single_role = False

    def get_context_data(self, **kwargs):
        context = super(TrixRoleSelectView, self).get_context_data(**kwargs)
        context['TRIX_ADMIN_DOCUMENTATION_URL'] = settings.TRIX_ADMIN_DOCUMENTATION_URL
        context['TRIX_ADMIN_DOCUMENTATION_LABEL'] = settings.TRIX_ADMIN_DOCUMENTATION_LABEL
        return context

    def get(self, request):
        if request.user.is_admin_on_anything():
            return super(TrixRoleSelectView, self).get(request)
        else:
            raise PermissionDenied
