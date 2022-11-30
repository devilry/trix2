from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from cradmin_legacy import crinstance
from cradmin_legacy import crmenu

from trix.trix_admin.views import roleselect
from trix.trix_core.models import Course
from .views import assignments
from .views import permalinks
from .views import statistics


class MenuItem(crmenu.MenuItem):
    """
    Extends default MenuItem with custom template.
    """
    template_name = 'trix_admin/menuitems.django.html'


class Menu(crmenu.Menu):
    """
    Menu on left side in admin pages.
    """
    template_name = 'trix_admin/menu.django.html'
    # Icon on top of the menu, mapped in 'css_icon_map.py'
    menuicon = 'wrench'

    def get_menuitem_class(self):
        """
        Override with custom MenuItems to add icons
        """
        return MenuItem

    def build_menu(self):
        self.add_menuitem(
            label=_('Frontpage'),
            url=reverse('trix_student_dashboard'),
            extra_context_data={'icon': 'home'}
        )
        self.add_menuitem(
            label=_('Course overview'),
            url=reverse('trix_course_dashboard'),
            extra_context_data={'icon': 'arrow-up'},
        )
        self.add_menuitem(
            label=_('Administrators'),
            url=reverse('trix_course_admin', kwargs={'course_id': self.request.cradmin_role.id}),
            extra_context_data={'icon': 'user'},
        )
        self.add_menuitem(
            label=_('Assignments'),
            url=self.appindex_url('assignments'),
            extra_context_data={'icon': 'database'},
        )
        self.add_menuitem(
            label=_('Permalinks'),
            url=self.appindex_url('permalinks'),
            extra_context_data={'icon': 'link'}
        )
        self.add_menuitem(
            label=_('Statistics'),
            url=self.appindex_url('statistics'),
            extra_context_data={'icon': 'chart-bar'},
        )


class CrAdminInstance(crinstance.BaseCrAdminInstance):
    id = 'trix_courseadmin'
    menuclass = Menu
    roleclass = Course
    rolefrontpage_appname = 'assignments'

    apps = [
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

    @classmethod
    def get_roleselect_view(cls):
        return login_required(roleselect.TrixRoleSelectView.as_view())
