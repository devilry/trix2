from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django_cradmin import crinstance
from django.core.urlresolvers import reverse
from trix.trix_admin.views import roleselect

from trix.trix_core.models import Course
# from .views import dashboard
from .views import assignments
from .views import permalinks
from .views import statistics


class CrAdminInstance(crinstance.BaseCrAdminInstance):
    id = 'trix_courseadmin'
    roleclass = Course
    rolefrontpage_appname = 'assignments'

    apps = [
        # ('dashboard', dashboard.App),
        ('assignments', assignments.App),
        ('permalinks', permalinks.App),
        ('statistics', statistics.App),
    ]

    def get_rolequeryset(self):
        queryset = Course.objects.all()
        if not self.request.user.is_admin:
            queryset = queryset.filter(admins=self.request.user)
        queryset = queryset.select_related('course_tag')
        return queryset

    def get_titletext_for_role(self, role):
        """
        Get a short title briefly describing the given ``role``.
        Remember that the role is a Course.
        """
        return role.course_tag.tag

    def get_menu_item_renderables(self):
        return [
            crmenu.LinkItemRenderable(
                label=_('Course overview'),
                url=self.cradmin_instance.roleselectview_url(),
                icon='arrow-up'),
            crmenu.LinkItemRenderable(
                label=_('Assignments'),
                url=self.appindex_url('assignments'),
                icon="database"),
            crmenu.LinkItemRenderable(
                label=_('Permalinks'),
                url=self.appindex_url('permalinks'),
                icon="link"),
            crmenu.LinkItemRenderable(
                label=_('Statistics'),
                url=self.appindex_url('statistics'),
                icon='bar-chart-o'),
        ]

    @classmethod
    def get_roleselect_view(cls):
        return login_required(roleselect.TrixRoleSelectView.as_view())
