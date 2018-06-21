from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from cradmin_legacy.views import roleselect


class TrixRoleSelectView(roleselect.RoleSelectView):
    pagetitle = _('Select a course to edit or create/edit assignments')
    template_name = 'trix_admin/roleselect.django.html'
    autoredirect_if_single_role = False

    def get_context_data(self, **kwargs):
        context = super(TrixRoleSelectView, self).get_context_data(**kwargs)
        context['TRIX_ADMIN_DOCUMENTATION_URL'] = settings.TRIX_ADMIN_DOCUMENTATION_URL
        context['TRIX_ADMIN_DOCUMENTATION_LABEL'] = settings.TRIX_ADMIN_DOCUMENTATION_LABEL
        return context
