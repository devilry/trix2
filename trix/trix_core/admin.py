from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Count, Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site

from trix.trix_core.models import Course, Tag, User


def set_administrators(modeladmin, request, queryset):
    queryset.update(is_admin=True)


set_administrators.short_description = _("Give admin access to the selected users")


def unset_administrators(modeladmin, request, queryset):
    queryset.update(is_admin=False)


unset_administrators.short_description = _("Remove admin access from the selected users")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'is_admin',
        'last_login',
    ]
    search_fields = ['email']
    list_filter = [
        'is_admin',
        'last_login',
    ]
    fields = ['email', 'is_admin']
    readonly_fields = ['last_login']
    actions = [set_administrators, unset_administrators]


class TagInUseFilter(admin.SimpleListFilter):
    title = _('tag is in use')
    parameter_name = 'tag_is_in_use'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(
                Q(assignment__count__gt=0) |
                Q(active_period_set__count__gt=0) |
                Q(course_set__count__gt=0)
            )
        if self.value() == 'no':
            return queryset.filter(
                Q(assignment__count=0) &
                Q(active_period_set__count=0) &
                Q(course_set__count=0)
            )


class TagAdminForm(forms.ModelForm):
    def clean_tag(self):
        tag = self.cleaned_data['tag']
        tag = Tag.split_commaseparated_tags(tag)
        self.cleaned_data['tag'] = tag[0]
        return self.cleaned_data['tag']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['tag']
    list_display = [
        'tag',
        'category',
        'get_assignment_count',
        'is_in_use'
    ]
    list_filter = [TagInUseFilter]
    form = TagAdminForm

    def get_queryset(self, request):
        return super(TagAdmin, self).get_queryset(request)\
            .annotate(
                Count('assignment', distinct=True),
                Count('active_period_set', distinct=True),
                Count('course_set', distinct=True))

    def get_assignment_count(self, tag):
        return str(tag.assignment__count)
    get_assignment_count.short_description = _('Number of assignments')
    get_assignment_count.admin_order_field = 'assignment__count'

    def is_in_use(self, tag):
        return (tag.assignment__count + tag.active_period_set__count + tag.course_set__count) > 0
    is_in_use.short_description = _('Is in use')
    is_in_use.boolean = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    course_id = None

    list_display = (
        'course_tag',
        'active_period',
        'get_admins',
        'get_owner',
    )
    search_fields = [
        'course_tag__tag',
        'description',
        'active_period__tag',
    ]
    filter_horizontal = ['admins', 'owner']
    raw_id_fields = ['course_tag', 'active_period']

    def get_admins(self, course):
        return ', '.join(str(user) for user in course.admins.all())
    get_admins.short_description = 'Admins'

    def get_owner(self, course):
        return ', '.join(str(user) for user in course.owner.all())
    get_owner.short_description = 'Owner'

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.course_id = obj.id
        return super(CourseAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Limit choices for owner to only those that are admins for the course.
        if db_field.name == "owner":
            if self.course_id:
                course = Course.objects.get(id=self.course_id)
                kwargs['queryset'] = course.admins
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_queryset(self, request):
        queryset = super(CourseAdmin, self).get_queryset(request)
        queryset = queryset\
            .select_related('course_tag', 'active_period')\
            .prefetch_related('admins')\
            .prefetch_related('owner')
        return queryset


# Fix for not being able to see the site ID.
admin.site.unregister(Site)

# Unregister group since it is not in use.
admin.site.unregister(Group)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'domain', 'name']
