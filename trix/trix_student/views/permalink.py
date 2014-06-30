import urllib
from django.views.generic import ListView
# from django import forms
from django.shortcuts import get_object_or_404

from trix.trix_core import models
from trix.trix_student.views.common import AssignmentListViewBase


class PermalinkView(AssignmentListViewBase):
    template_name = "trix_student/permalink.django.html"
    paginate_by = 20

    def get(self, request, **kwargs):
        self.permalink_id = kwargs['permalink_id']
        self.permalink = get_object_or_404(models.Permalink, id=self.permalink_id)
        
        self.all_available_assignments = models.Assignment.objects.all()
        #TODO filter

        return super(PermalinkView, self).get(request, **kwargs)

    def get_already_selected_tags(self):
        return []
        #self.permalink.tags.values_list('tag', flat=True)

    def get_nonremoveable_tags(self):
        return self.permalink.tags.values_list(flat=True)

    def get_context_data(self, **kwargs):
        context = super(PermalinkView, self).get_context_data(**kwargs)

        context['permalink'] = self.permalink

        return context