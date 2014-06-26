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


class CourseDetailView(ListView):
    template_name = "trix_student/course.django.html"
    paginate_by = 20
    context_object_name = 'assignment_list'

    def get(self, request, course_id):
        self.course_id = course_id
        self.course = get_object_or_404(models.Course, id=self.course_id)
        
        self.all_available_assignments = models.Assignment.objects\
            .filter_by_tag(self.course.course_tag)\
            .filter_by_tag(self.course.active_period)

        self.selected_tags = self._get_selected_tags()
        self.selectable_tags = self._get_selectable_tags()
        self.non_removeable_tags = self.get_nonremovable_tags()

        return super(CourseDetailView, self).get(request, course_id)

    def get_queryset(self):
        assignments = self.all_available_assignments
        if self.selected_tags:
            for tagstring in self.selected_tags:
                assignments = assignments.filter(tags__tag=tagstring)
        return assignments

    def _get_selectable_tags(self):
        already_selected_tags = [
            self.course.course_tag.tag,
            self.course.active_period.tag
        ] + self.selected_tags

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

    def get_nonremovable_tags(self):
        return [self.course.active_period]

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)

        context['non_removeable_tags'] = [self.course.active_period]
        context['object'] = self.course
        context['selected_tags'] = self.selected_tags
        context['selectable_tags'] = self.selectable_tags
        # context['tag_select_form'] = TagSelectForm(choices=self.tags)
        return context
