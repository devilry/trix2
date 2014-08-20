from django.contrib import admin
from trix.trix_core import models


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'is_active',
        'is_admin',
        'last_login',
    ]
    search_fields = ['email']
    list_filter = [
        'is_active',
        'is_admin',
        'last_login',
    ]
    fields = ['email', 'is_admin', 'is_active']
    readonly_fields = ['last_login']

admin.site.register(models.User, UserAdmin)


class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'get_tags',
        'created_datetime',
        'lastupdate_datetime',
    )
    search_fields = ['title', 'tags__tag']
    filter_horizontal = ['tags']
    list_filter = [
        'created_datetime',
        'lastupdate_datetime',
        'tags',
    ]

    def get_tags(self, course):
        return u','.join(tag.tag for tag in course.tags.all())
    get_tags.short_description = 'Tags'

    def get_queryset(self, request):
        queryset = super(AssignmentAdmin, self).get_queryset(request)
        queryset = queryset.prefetch_related('tags')
        return queryset


admin.site.register(models.Assignment, AssignmentAdmin)


class TagAdmin(admin.ModelAdmin):
    search_fields = ['tag']
admin.site.register(models.Tag, TagAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'course_tag',
        'active_period',
        'get_admins',

    )
    search_fields = [
        'course_tag__tag',
        'description',
        'active_period__tag',
    ]
    filter_horizontal = ['admins']
    raw_id_fields = ['course_tag', 'active_period']

    def get_admins(self, course):
        return u','.join(unicode(user) for user in course.admins.all())
    get_admins.short_description = 'Admins'

    def get_queryset(self, request):
        queryset = super(CourseAdmin, self).get_queryset(request)
        queryset = queryset\
            .select_related('course_tag', 'active_period')\
            .prefetch_related('admins')
        return queryset

admin.site.register(models.Course, CourseAdmin)


class PermalinkAdmin(admin.ModelAdmin):
    list_display = (
        'course',
        'title',
        'get_tags',
    )
    search_fields = [
        'tags__tag',
        'title',
        'description',
        'course__course_tag__tag',
    ]
    filter_horizontal = ['tags']
    raw_id_fields = ['course']
    list_filter = [
        'tags',
    ]

    def get_tags(self, permalink):
        return u','.join(tag.tag for tag in permalink.tags.all())
    get_tags.short_description = 'Tags'

    def get_queryset(self, request):
        queryset = super(PermalinkAdmin, self).get_queryset(request)
        queryset = queryset\
            .select_related('course', 'course__course_tag')\
            .prefetch_related('tags')
        return queryset


admin.site.register(models.Permalink, PermalinkAdmin)
