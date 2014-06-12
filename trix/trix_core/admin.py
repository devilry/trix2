from django.contrib import admin
from trix.trix_core import models

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.User, UserAdmin)

class AssignmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Assignment, AssignmentAdmin)

class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Tag, TagAdmin)

class CourseAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Course, CourseAdmin)

class PermalinkAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Permalink, PermalinkAdmin)