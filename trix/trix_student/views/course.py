from django.views.generic import DetailView
from trix.trix_core import models

from django import forms

class TagSelectForm(forms.Form):
    tag_choice = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        super(TagSelectForm, self).__init__(*args, **kwargs)
        self.fields['tag_choice'].queryset = choices

class CourseDetailView(DetailView):
    model = models.Course
    pk_url_kwarg = 'course_id'
    template_name = "trix_student/course.django.html"

    selected_tags = None

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        assignments = models.Assignment.objects.filter_by_tag(obj.course_tag)\
            .filter_by_tag(obj.active_period)

        
        tags = models.Tag.objects.filter(assignment__in=assignments).distinct()
        tags = tags.exclude(id__in=[x.id for x in (obj.course_tag, obj.active_period)])

        tag_list_from_url = self.request.GET.get('tags', None)
        if tag_list_from_url:
            tag_list_from_url = tag_list_from_url.split(',')

        # Show the non removeable tags as disabled
        context['non_removeable_tags'] = [obj.active_period]

        context['assignment_list'] = assignments
        context['tags'] = tags
        context['tag_select_form'] = TagSelectForm(choices=tags)
        return context

