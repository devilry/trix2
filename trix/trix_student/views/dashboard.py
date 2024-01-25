from typing import Any
from django.conf import settings
from django.db.models.query import QuerySet
from django.db.models import Q
from trix.trix_core import models
from trix.trix_student.views import base


class CourseListView(base.TrixListViewBase):
    model = models.Course
    template_name = "trix_student/dashboard.django.html"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['TRIX_STUDENT_GETTINGSTARTEDGUIDE_URL'] =\
            settings.TRIX_STUDENT_GETTINGSTARTEDGUIDE_URL
        return context

    def get(self, request, **kwargs):
        self.user = request.user
        return super().get(request, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        if self.user.is_anonymous:
            return models.Course.objects.filter(visible=True)
        if self.user.is_admin:
            return super().get_queryset()
        return models.Course.objects.filter(Q(visible=True) | Q(admins=self.user))
