from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from trix.trix_core import models
from trix.trix_student.views.common import AssignmentListViewBase


class PermalinkView(AssignmentListViewBase):
    template_name = "trix_student/permalink.django.html"
    paginate_by = 20

    def get(self, request, **kwargs):
        self.permalink_id = kwargs['permalink_id']
        self.permalink = get_object_or_404(models.Permalink, id=self.permalink_id)
        return super(PermalinkView, self).get(request, **kwargs)

    def _get_user_is_admin(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                return True
            else:
                return self.permalink.course.admins.filter(id=self.request.user.id)
        else:
            return False

    def get_all_available_assignments(self):
        return models.Assignment.objects\
            .filter_by_tags(self.permalink.tags.all())

    def get_already_selected_tags(self):
        already_selected_tags = []
        for tag in self.get_nonremoveable_tags():
            already_selected_tags.append(tag)
        return already_selected_tags

    def get_nonremoveable_tags(self):
        return self.permalink.tags.values_list('tag', flat=True)

    def get_context_data(self, **kwargs):
        context = super(PermalinkView, self).get_context_data(**kwargs)
        context['permalink'] = self.permalink
        context['course'] = self.permalink.course
        return context


class PermalinkListView(ListView):
    model = models.Permalink
    template_name = "trix_student/permalink_list.django.html"
