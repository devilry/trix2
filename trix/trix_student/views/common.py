import urllib
from django.views.generic import ListView
# from django import forms
from django.shortcuts import get_object_or_404

from trix.trix_core import models

class AssignmentListViewBase(ListView):
    paginate_by = 100
    context_object_name = 'assignment_list'
    already_selected_tags = []

    def get(self, request, **kwargs):

        self.selected_tags = self._get_selected_tags()
        self.selectable_tags = self._get_selectable_tags()
        self.non_removeable_tags = self.get_nonremoveable_tags()

        return super(AssignmentListViewBase, self).get(request, **kwargs)
        
    def get_queryset(self):
        assignments = self.all_available_assignments
        if self.selected_tags:
            for tagstring in self.selected_tags:
                assignments = assignments.filter(tags__tag=tagstring)
        return assignments

    def _get_user_is_admin(self):
        if self.request.user.is_authenticated():
            if self.request.user.is_admin:
                return True
            else:
                return self.course.admins.filter(id=self.request.user.id)
        else:
            return False

    def _get_assignments_solved_percentage(self):
        num_solved = models.AssignmentSolution.objects.filter(assignment__in=self.get_queryset()).count()
        num_total = self.get_queryset().count()
        return int(num_solved / float(num_total) * 100)

    def _get_selectable_tags(self):
        already_selected_tags = self.get_already_selected_tags() + self.selected_tags

        tags = models.Tag.objects\
            .filter(assignment__in=self.get_queryset())\
            .exclude(tag__in=already_selected_tags)\
            .order_by('tag')\
            .distinct()\
            .values_list('tag', flat=True)
        return tags

    def _get_selected_tags(self):
        tags_string = self.request.GET.get('tags', None)
        tags = []
        if tags_string:
            tags = tags_string.split(',')
            tags.sort()
        return tags

    def get_context_data(self, **kwargs):
        context = super(AssignmentListViewBase, self).get_context_data(**kwargs)

        context['non_removeable_tags'] = self.non_removeable_tags
        context['selected_tags'] = self.selected_tags
        context['selectable_tags'] = self.selectable_tags
        context['user_is_admin'] = self._get_user_is_admin()
        context['urlencoded_success_url'] = urllib.urlencode({
            'success_url': self.request.get_full_path()})

        context['assignments_solved_percentage'] = self._get_assignments_solved_percentage()
        # context['assignments_solved_percentage'] = 81
        return context

    def get_nonremoveable_tags(self):
        raise NotImplementedError()

    def get_already_selected_tags(self):
        raise NotImplementedError()
