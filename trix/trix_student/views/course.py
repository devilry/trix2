import urllib
from django.views.generic import ListView
# from django import forms
from django.shortcuts import get_object_or_404

from trix.trix_core import models


# class TagSelectForm(forms.Form):
#     tag_choice = forms.ModelChoiceField(queryset=None)

#     def __init__(self, *args, **kwargs):
#         choices = kwargs.pop('choices')
#         super(TagSelectForm, self).__init__(*args, **kwargs)
#         self.fields['tag_choice'].queryset = choices

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

class CourseDetailView(AssignmentListViewBase):
    template_name = "trix_student/course.django.html"
    paginate_by = 20

    def get(self, request, **kwargs):
        self.course_id = kwargs['course_id']
        self.course = get_object_or_404(models.Course, id=self.course_id)
        
        self.all_available_assignments = models.Assignment.objects\
            .filter_by_tag(self.course.course_tag)\
            .filter_by_tag(self.course.active_period)

        return super(CourseDetailView, self).get(request, **kwargs)

    def get_already_selected_tags(self):
        already_selected_tags = [
            self.course.course_tag.tag,
            self.course.active_period.tag
        ]
        return already_selected_tags

    def get_nonremoveable_tags(self):
        return [self.course.course_tag, self.course.active_period]

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)

        context['course'] = self.course

        return context

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